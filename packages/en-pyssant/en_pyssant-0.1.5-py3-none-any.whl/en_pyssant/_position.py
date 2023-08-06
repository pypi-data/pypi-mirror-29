# -*- coding: utf-8 -*-
#
# Copyright (C) 2017-2018  Carmen Bianca Bakker <carmen@carmenbianca.eu>
# Copyright (C) 2017  Stefan Bakker <s.bakker777@gmail.com>
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

"""Representation of chess position."""

from collections import namedtuple
from io import StringIO
from typing import Optional, Type

from ._board import Board, DictBoard  # pylint: disable=unused-import
from ._core import Side, Square
from ._util import validate_fen


class CastlingAvailability(
        namedtuple('CastlingAvailability', ['kingside', 'queenside'])):
    """Tuple of kingside and queenside castling availability.

    >>> castling = CastlingAvailability(True, True)
    >>> castling.kingside
    True
    """
    __slots__ = ()

    def __new__(
            cls,
            kingside: bool,
            queenside: bool) -> 'CastlingAvailability':
        """:param kingside: Whether kingside castling is available.
        :param queenside: Whether queenside castling is available.
        """
        return super().__new__(cls, kingside, queenside)


class Position(
        namedtuple(
            'Position',
            [
                'board', 'side_to_play', 'castling', 'en_passant_target',
                'half_move_clock', 'move_count'
            ])):
    """Tuple that represents a snapshot of the state of a chess game.  The
    structure explicitly matches Forsyth-Edwards Notation as well as possible.

    .. IMPORTANT::
        A chess position is a *state*, not a location.

    >>> Position(
    ...     DictBoard(),
    ...     Side.WHITE,
    ...     {Side.WHITE: CastlingAvailability(True, True),
    ...     Side.BLACK: CastlingAvailability(True, True)},
    ...     None,
    ...     0,
    ...     1)
    ...
    rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
    >>> Position()  # No arguments
    rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
    """
    __slots__ = ()

    # pylint: disable=too-many-arguments
    def __new__(cls,
                board: Board = None,
                side_to_play: Side = Side.WHITE,
                castling: CastlingAvailability = None,
                en_passant_target: Optional[Square] = None,
                half_move_clock: int = 0,
                move_count: int = 1) -> 'Position':
        """:param board: Board representation.
        :param side_to_play: Side to play.
        :param castling: Castling rights of black and white.
        :param en_passant_target: Square 'behind' a pawn that has moved
            two squares in the previous turn.
        :param half_move_clock: Number of halfmoves since last capture or
            pawn advance.
        :param move_count: Amount of moves since start.  Increments after
            black's move.
        """
        if board is None:
            board = DictBoard()
        if castling is None:
            castling = {Side.WHITE: CastlingAvailability(True, True),
                        Side.BLACK: CastlingAvailability(True, True)}
        if (en_passant_target is not None
                and not isinstance(en_passant_target, Square)):
            en_passant_target = Square(en_passant_target)
        return super().__new__(cls, board, side_to_play, castling,
                               en_passant_target, half_move_clock, move_count)

    @classmethod
    def from_fen(
            cls,
            fen: str,
            board_cls: Type[Board] = DictBoard) -> 'Position':
        """Generate a :class:`Position` from a Forsyth-Edwards Notation string.

        >>> fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        >>> Position.from_fen(fen)
        rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

        :param fen: Forsyth-Edwards Notation.
        :param board_cls: Type that will be used for :attr:`board`.
        :return: A position.
        :raise ValueError: Input is invalid
        """
        splitted = fen.split()

        if not validate_fen(fen):
            raise ValueError('{} is not a valid notation'.format(fen))

        board = board_cls.from_fen(splitted[0])

        side_to_play = Side.WHITE if splitted[1] == 'w' else Side.BLACK

        castling = {
            Side.WHITE: CastlingAvailability('K' in splitted[2],
                                             'Q' in splitted[2]),
            Side.BLACK: CastlingAvailability('k' in splitted[2],
                                             'q' in splitted[2])
        }

        en_passant_target = None if splitted[3] == '-' else splitted[3]

        half_move_clock = int(splitted[4])
        move_count = int(splitted[5])

        return cls(board, side_to_play, castling, en_passant_target,
                   half_move_clock, move_count)

    def pretty(self) -> str:
        """
        >>> print(Position().pretty())
          A B C D E F G H
        8 r n b q k b n r
        7 p p p p p p p p
        6 . . . . . . . .
        5 . . . . . . . .
        4 . . . . . . . .
        3 . . . . . . . .
        2 P P P P P P P P
        1 R N B Q K B N R
        <BLANKLINE>
        FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

        :return: A pretty representation of the position.
        """
        result = StringIO()
        result.write(self.board.pretty())
        result.write('\n\n')
        result.write('FEN: {}'.format(str(self)))
        return result.getvalue()

    def __repr__(self) -> str:
        board = repr(self.board)
        side_to_play = 'w' if self.side_to_play == Side.WHITE else 'b'
        # Would like to simplify this castling portion.
        castling_white = ''.join(['K' if self.castling[Side.WHITE].kingside
                                  else '',
                                  'Q' if self.castling[Side.WHITE].queenside
                                  else ''])
        castling_black = ''.join(['k' if self.castling[Side.BLACK].kingside
                                  else '',
                                  'q' if self.castling[Side.BLACK].queenside
                                  else ''])
        castling = ''.join([castling_white, castling_black])
        if not castling:
            castling = '-'
        en_passant_target = (self.en_passant_target if self.en_passant_target
                             else '-')
        half_move_clock = str(self.half_move_clock)
        move_count = str(self.move_count)
        return ' '.join([board, side_to_play, castling, en_passant_target,
                         half_move_clock, move_count])
