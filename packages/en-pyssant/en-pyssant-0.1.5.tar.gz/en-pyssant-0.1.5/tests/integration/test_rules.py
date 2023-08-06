# -*- coding: utf-8 -*-
#
# Copyright (C) 2017-2018  Carmen Bianca Bakker <carmen@carmenbianca.eu>
#
# This file is part of En Pyssant, available from its original location:
# <https://gitlab.com/carmenbianca/en-pyssant>.
#
# En Pyssant is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# En Pyssant is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with En Pyssant.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0+

"""Integrated tests for en_pyssant.rules"""

# pylint: disable=no-self-use,invalid-name

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pytest  # pylint: disable=unused-import

from en_pyssant import (Gameover, HistoryRecord, Move, MoveFlag, Piece,
                        Position, Side, Square, Type)
from en_pyssant._util import ALL_SQUARES, opponent
from en_pyssant.rules import (attacked, do_move, is_check, is_checkmate,
                              is_draw, is_fifty_move, is_gameover,
                              is_insufficient_material, is_stale, is_stalemate,
                              is_threefold_repetition, loser, moves, winner)


class TestAttacked:
    """All tests for :func:`attacked`."""
    # pylint: disable=undefined-variable

    @staticmethod
    def only_targets_attacked(position, attacking_side, targets):
        """Convenience function.  Check if, on the whole board, only *targets*
        are in check.
        """
        for square in ALL_SQUARES:
            result = attacked(position, attacking_side, square)
            if square in targets:
                assert result
            else:
                assert not result

    def test_initial(self, b):
        """All the squares that are under siege on an initial chess board are
        correctly identified by :func:`attacked`.
        """
        white_under_siege = ['{}{}'.format(char, num) for char in 'abcdefgh'
                             for num in '23']
        white_under_siege.extend(['b1', 'c1', 'd1', 'e1', 'f1', 'g1'])
        black_under_siege = ['{}{}'.format(char, num) for char in 'abcedfgh'
                             for num in '67']
        black_under_siege.extend(['b8', 'c8', 'd8', 'e8', 'f8', 'g8'])

        position = Position(board=b.INITIAL_BOARD)

        self.only_targets_attacked(position, Side.WHITE, white_under_siege)
        self.only_targets_attacked(position, Side.BLACK, black_under_siege)

    def test_en_passant(self, b):
        """Pawns that can be captured via en passant are attacked according to
        :func:`attacked`.
        """
        variables = [
            # Side to play (attacking side), en_passant_target, square of pawn
            (Side.BLACK, 'a3', 'a4'),
            (Side.BLACK, 'c3', 'c4'),
            (Side.WHITE, 'f6', 'f5'),
            (Side.WHITE, 'h6', 'h5'),
        ]

        for tup in variables:
            position = Position(board=b.EN_PASSANT_BOARD,
                                side_to_play=tup[0],
                                en_passant_target=tup[1])
            assert attacked(position, tup[0], tup[2])

    def test_king_attack_ray(self, b):
        """The king's ray of attack is correctly identified according to
        :func:`attacked`.
        """
        position = Position(board=b.KING_ROOK_BOARD)

        targets = [
            'a8',
            'b8',
            'c8',
            'a7',
            'c7',
            'a6',
            'b6',
            'c6',
        ]

        self.only_targets_attacked(position, Side.BLACK, targets)

    def test_rook_attack_ray(self, b):
        """The rook's ray of attack is correctly identified according to
        :func:`attacked`.

        Subsequently, the king on the board blocks the path to the square
        behind it.
        """
        position = Position(board=b.KING_ROOK_BOARD)

        targets = [
            # downwards
            'b7',
            'b6',
            'b5',
            'b4',
            'b2',
            'b1',
            # to the right
            'a3',
            'c3',
            'd3',
            'e3',
            'f3',
            'g3',
            'h3',
        ]

        self.only_targets_attacked(position, Side.WHITE, targets)

    def test_queen_attack_ray(self, b):
        """The queen's ray of attack is correctly identified according to
        :func:`attacked`.

        Subsequently, the pawn and bishop on the board block the path to the
        square behind it.
        """
        position = Position(board=b.QUEEN_BISHOP_BOARD)

        targets = [
            # downwards
            'c8',
            'c7',
            'c5',
            'c4',
            'c3',
            'c2',
            # to the right
            'a6',
            'b6',
            'd6',
            'e6',
            'f6',
            'g6',
            'h6',
            # from top-left to bottom-right
            'a8',
            'b7',
            'd5',
            'e4',
            'f3',
            # from bottom-left to top-right
            'a4',
            'b5',
            'd7',
            'e8',
        ]

        self.only_targets_attacked(position, Side.BLACK, targets)

    def test_bishop_attack_ray(self, b):
        """The bishop's ray of attack is correctly identified according to
        :func:`attacked`.

        Subsequently, the queen on the board blocks the path to the square
        behind it.
        """
        position = Position(board=b.QUEEN_BISHOP_BOARD)

        targets = [
            # from top-left to bottom-right
            'c6',
            'd5',
            'e4',
            'g2',
            'h1',
            # from bottom-left to top-right
            'd1',
            'e2',
            'g4',
            'h5',
        ]
        # The pawn also has targets
        targets.extend(['b3', 'd3'])

        self.only_targets_attacked(position, Side.WHITE, targets)

    def test_knight_attack_ray(self, b):
        """The knight's ray of attack is correctly identified according to
        :func:`attacked`.  The knight is able to jump over pieces.
        """

        position = Position(board=b.KNIGHT_BOARD)

        # Clockwise
        targets = [
            'b8',
            'd8',
            'e7',
            'e5',
            'd4',
            'b4',
            'a5',
            'a7',
        ]

        self.only_targets_attacked(position, Side.WHITE, targets)


class TestMoves:
    """All tests for :func:`moves`."""
    # pylint: disable=undefined-variable

    def test_castling_regular(self, b):
        """Test if castling moves are returned by :func:`moves`."""
        for side in Side:
            position = Position(board=b.CASTLING_BOARD, side_to_play=side)
            legal_moves = list(moves(position))
            home_rank = 8 if side == Side.BLACK else 1
            king_square = Square('e{}'.format(home_rank))
            move_kingside = Move(king_square, king_square.right().right(),
                                 position.board[king_square],
                                 flags={MoveFlag.KINGSIDE_CASTLING,
                                        MoveFlag.NON_CAPTURE})
            move_queenside = Move(king_square, king_square.left().left(),
                                  position.board[king_square],
                                  flags={MoveFlag.QUEENSIDE_CASTLING,
                                         MoveFlag.NON_CAPTURE})
            assert move_kingside in legal_moves
            assert move_queenside in legal_moves

    def test_castling_king_in_check(self, b):
        """Cannot castle when king is in check."""
        for side in Side:
            board = b.CASTLING_BOARD.put(
                'e4', Piece(Type.ROOK, opponent(side))
            )
            position = Position(board=board, side_to_play=side)
            legal_moves = moves(position)
            for move in legal_moves:
                assert MoveFlag.KINGSIDE_CASTLING not in move.flags
                assert MoveFlag.QUEENSIDE_CASTLING not in move.flags

    def test_castling_path_in_check(self, b):
        """Cannot castle when path (or destination) is in check."""
        for side in Side:
            square_map = {
                'e2': MoveFlag.QUEENSIDE_CASTLING,
                'e3': MoveFlag.QUEENSIDE_CASTLING,
                'e5': MoveFlag.KINGSIDE_CASTLING,
                'e6': MoveFlag.KINGSIDE_CASTLING,
            }
            for square, flag in square_map.items():
                board = b.CASTLING_BOARD.put(square, Piece(Type.ROOK,
                                                           opponent(side)))
                position = Position(board=board, side_to_play=side)
                legal_moves = moves(position)
                for move in legal_moves:
                    assert flag not in move.flags

    def test_stalemate_no_moves(self, b):
        """There are no legal moves in a stalemate."""
        position = Position(board=b.STALEMATE_BOARD)
        legal_moves = list(moves(position))
        assert not legal_moves

    def test_pinned(self, b):
        """A piece is pinned if moving it would result in a checkmate."""
        board = b.STALEMATE_BOARD.put('e3', Piece(Type.KNIGHT, Side.WHITE))
        board = board.put('e4', Piece(Type.ROOK, Side.BLACK))
        position = Position(board=board)
        legal_moves = list(moves(position))
        assert not legal_moves

    def test_en_passant(self, b):
        """En passant moves are correctly registered as legal moves."""
        for side in Side:
            squares = ('f6', 'h6') if side == Side.WHITE else ('a3', 'c3')
            for square in squares:
                position = Position(
                    board=b.EN_PASSANT_BOARD,
                    side_to_play=side,
                    en_passant_target=square
                )
                legal_moves = moves(position)
                count = 0
                for move in legal_moves:
                    if MoveFlag.EN_PASSANT_CAPTURE in move.flags:
                        count += 1
                assert count == 1

    def test_pawn_path_blocked(self, b):
        """If a piece stands in front of a pawn, it cannot advance."""
        squares = ('a3', 'a4')
        for square in squares:
            board = b.PAWN_BOARD.put(square, Piece(Type.ROOK, Side.BLACK))
            position = Position(board=board)
            legal_moves = list(moves(position))
            for move in legal_moves:
                assert move.destination != square
            if square == 'a3':
                assert not legal_moves

    def test_promotion(self, b):
        """A pawn at the end of the board yields promotion moves."""
        board = b.PROMOTION_BOARD.put('b8', Piece(Type.ROOK, Side.BLACK))
        position = Position(board=board)
        for move in moves(position):
            assert MoveFlag.PROMOTION in move.flags
            assert move.promotion


class TestDoMove:
    """All tests for :func:`do_move`."""
    # pylint: disable=undefined-variable

    def test_all_legal_moves(self, b):
        """For sanity: Test whether do_move correctly executes all legal moves
        in the starting position.
        """
        position = Position(board=b.INITIAL_BOARD)
        for move in moves(position):
            do_move(position, move)

    def test_invalid_move(self, b):
        """An error is raised when an invalid move is given."""
        with pytest.raises(ValueError):
            do_move(Position(board=b.INITIAL_BOARD), Move('a1', 'h8'))

    def test_promotion_unspecified(self, b):
        """Pawn is promoted to queen if no promotion is specified in *move*."""
        position = do_move(Position(board=b.PROMOTION_BOARD), Move('a7', 'a8'))
        assert position.board['a8'].type == Type.QUEEN

    def test_promotion_specified(self, b):
        """Pawn is promoted to specified piece."""
        for target in (Type.KNIGHT, Type.BISHOP, Type.ROOK, Type.QUEEN):
            position = do_move(Position(board=b.PROMOTION_BOARD),
                               Move('a7', 'a8', promotion=target))
            assert position.board['a8'].type == target

    def test_captured(self, b):
        """A captured piece is removed from the board."""
        position = do_move(Position(board=b.CASTLING_BOARD), Move('a1', 'a8'))
        assert position.board['a8'] == Piece(Type.ROOK, Side.WHITE)
        assert position.board['a1'] is None

    def test_en_passant_capture(self, b):
        """An en passant capture results in the removal of the captured pawn.
        """
        position = do_move(Position(board=b.EN_PASSANT_BOARD,
                                    en_passant_target='h6'), Move('g5', 'h6'))
        assert position.board['h6'] == Piece(Type.PAWN, Side.WHITE)
        assert position.board['g5'] is None
        assert position.board['h5'] is None

    def test_castling_kingside(self, b):
        """The king and rook are in the right place after a kingside castle."""
        position = do_move(Position(board=b.CASTLING_BOARD), Move('e1', 'g1'))
        assert position.board['g1'] == Piece(Type.KING, Side.WHITE)
        assert position.board['f1'] == Piece(Type.ROOK, Side.WHITE)

    def test_castling_queenside(self, b):
        """The king and rook are in the right place after a queenside castle.
        """
        position = do_move(Position(board=b.CASTLING_BOARD), Move('e1', 'c1'))
        assert position.board['c1'] == Piece(Type.KING, Side.WHITE)
        assert position.board['d1'] == Piece(Type.ROOK, Side.WHITE)

    def test_move_is_san(self, position):
        """The function also accepts a SAN string for its move."""
        position = do_move(position, 'a3')
        assert position.board['a3'] == Piece(Type.PAWN, Side.WHITE)


class TestGameover:
    """Tests for all game-over functions."""
    # pylint: disable=undefined-variable

    def test_initial_board(self, b):
        """The initial board tests negative for all these things."""
        position = Position(board=b.INITIAL_BOARD)
        assert not is_check(position)
        assert not is_checkmate(position)
        assert not is_draw(position)
        assert not is_fifty_move(position)
        assert not is_gameover(position)
        assert not is_insufficient_material(position)
        assert not is_stale(position)
        assert not is_stalemate(position)
        assert not is_threefold_repetition([])

    def test_is_checkmate(self, b):
        """:func:`is_checkate` correctly identifies a board that is in
        checkmate.  That same board is also stale, check and not stalemate.
        """
        position = Position(board=b.CHECKMATE_BOARD)
        assert is_checkmate(position)
        assert is_check(position)
        assert is_stale(position)
        assert not is_stalemate(position)
        assert not is_draw(position)
        assert is_gameover(position) == Gameover.CHECKMATE

    def test_not_fifty_move(self):
        """If half move clock is under fifty, the fifty-move rule is not
        triggered.
        """
        for i in range(50):
            position = Position(half_move_clock=i)
            assert not is_fifty_move(position)
            assert not is_gameover(position)

    def test_fifty_move(self):
        """If half move clock is fifty or over, the fifty-move rule is
        triggered.
        """
        for i in range(50, 100):
            position = Position(half_move_clock=i)
            assert is_fifty_move(position)
            assert is_draw(position)
            assert is_gameover(position) == Gameover.FIFTY_MOVE

    def test_insufficient_material_two_kings(self, b):
        """There is insufficient material when there are only two kings on the
        board.
        """
        position = Position(board=b.KING_V_KING)
        assert is_insufficient_material(position)
        assert is_draw(position)
        assert is_gameover(position) == Gameover.INSUFFICIENT_MATERIAL

    def test_insufficient_material_two_kings_plus_knight(self, b):
        """There is insufficient material when a king is faced off against a
        king and a knight.
        """
        position = Position(board=b.KING_KNIGHT_V_KING)
        assert is_insufficient_material(position)
        assert is_draw(position)
        assert is_gameover(position) == Gameover.INSUFFICIENT_MATERIAL

    def test_insufficient_material_kings_and_bishops(self, b):
        """There is insufficient material when there are only kings and bishops
        on the board, and the bishops all occupy the same square colour.
        """
        position = Position(board=b.KING_BISHOP_V_KING_BISHOP)
        assert is_insufficient_material(position)
        assert is_draw(position)
        assert is_gameover(position) == Gameover.INSUFFICIENT_MATERIAL

    def test_is_stalemate(self, b):
        """:func:`is_stalemate` correctly identifies a board that is in
        stalemate.  That same board is also stale, not check, and not
        checkmate.
        """
        position = Position(board=b.STALEMATE_BOARD)
        assert is_stalemate(position)
        assert is_stale(position)
        assert not is_checkmate(position)
        assert not is_check(position)
        assert is_draw(position)
        assert is_gameover(position) == Gameover.STALEMATE

    def test_threefold_repetition(self, b):
        """A history containing three identical positions is in threefold
        repetition.

        The positions aren't 100% identical. The move count and half-move clock
        differ.
        """
        history = [
            HistoryRecord(
                Position(
                    board=b.INITIAL_BOARD,
                    move_count=i,
                    half_move_clock=i),
                None)
            for i in range(3)
        ]
        assert is_threefold_repetition(history)
        assert is_draw(Position(), history)
        assert (is_gameover(Position(), history) ==
                Gameover.THREEFOLD_REPETITION)

    def test_threefold_repetition_none(self):
        """:func:`test_threefold_repetition` returns False if no argument is
        given.
        """
        assert not is_threefold_repetition()
        assert not is_draw(Position())
        assert not is_gameover(Position())

    def test_winner_loser(self, b):
        """:func:`winner` and :func:`loser` return the correct winner and loser
        in CHECKMATE_BOARD.
        """
        position = Position(board=b.CHECKMATE_BOARD, side_to_play=Side.WHITE)
        assert winner(position) == Side.BLACK
        assert loser(position) == Side.WHITE

    def test_no_winner_loser(self, b):
        """There is no winner or loser in STALEMATE_BOARD."""
        position = Position(board=b.STALEMATE_BOARD, side_to_play=Side.WHITE)
        assert winner(position) is None
        assert loser(position) is None
