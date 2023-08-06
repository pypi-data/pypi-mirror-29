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

"""Unit tests for Board."""

# pylint: disable=invalid-name

import pytest

from en_pyssant import Piece, Side, Type
from en_pyssant._util import ALL_SQUARES


def test_get_is_getitem(board):
    """Board.get and Board.__getitem__ return the same value."""
    assert board['a1'] == board.get('a1')


def test_no_setitem(board):
    """Board.__setitem__ is not implemented."""
    with pytest.raises(TypeError):
        board['a1'] = None


def test_get_a1(board):
    """Square a1 is a white rook."""
    assert board['a1'] == Piece(Type.ROOK, Side.WHITE)


def test_get_h8(board):
    """Square h8 is a black rook."""
    assert board['h8'] == Piece(Type.ROOK, Side.BLACK)


def test_correct_initial_board(board):
    """The board matches an initial chess board."""
    pieces = [Type(char) for char in 'rnbqkbnrpppppppp']
    # Black and empty squares
    for i, (_, piece) in enumerate(board.all_pieces()):
        if i < 16:
            assert piece == Piece(pieces[i], Side.BLACK)
        if 16 <= i < 48:
            assert piece is None
        if i == 48:
            break
    squares = list(board.all_pieces())
    white_squares = [squares[i] for i in range(56, 64)]
    white_squares.extend(squares[i] for i in range(48, 56))
    # White squares
    for i, (_, piece) in enumerate(white_squares):
        assert piece == Piece(pieces[i], Side.WHITE)


def test_count_squares(board):
    """There are 32 pieces and 32 empty squares on a default board."""
    count_pieces = 0
    count_empty = 0
    for square in ALL_SQUARES:
        if board[square]:
            count_pieces += 1
        else:
            count_empty += 1
    assert count_pieces == count_empty == 32


def test_clear(board):
    """If you put None on every square, verify that the board is indeed empty.
    """
    for square in ALL_SQUARES:
        board = board.put(square, None)
    for square in ALL_SQUARES:
        assert board[square] is None


def test_put_all_pieces(board):
    """Board.put can put all pieces of both sides on all squares."""
    for square in ALL_SQUARES:
        for side in Side:
            for type_ in Type:
                piece = Piece(type_, side)
                assert board.put(square, piece)[square] == piece


def test_repr_default_board(board):
    """Board.__repr__ returns the initial board in Forsyth-Edwards Notation."""
    assert repr(board) == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'


def test_repr_empty_board(board):
    """Board.__repr__ on an empty board returns the correct representation."""
    for square in ALL_SQUARES:
        board = board.put(square, None)
    assert repr(board) == '8/8/8/8/8/8/8/8'


def test_repr_empty_squares_are_numbers(board):
    """Board.__repr__ condenses empty squares in a rank to numbers."""
    rank = 6
    files = 'abcdefgh'
    for i, file_ in enumerate(files):
        square = '{}{}'.format(file_, rank)
        new_board = board.put(square, Piece(Type.PAWN, Side.WHITE))
        rank_string = repr(new_board).split('/')[8 - rank]
        assert rank_string == '{}{}{}'.format(
            i if i else '',
            'P',
            7 - i if i != 7 else '')


def test_repr_alternating_numbers_and_pieces(board):
    """A rank in Board.__repr__ allows for alternating numbers and pieces.
    e.g., 1r1r1r1r.
    """
    rank = 6
    files = 'bdfh'
    for file_ in files:
        square = '{}{}'.format(file_, rank)
        board = board.put(square, Piece(Type.ROOK, Side.BLACK))
    assert repr(board).split('/')[8 - rank] == '1r1r1r1r'


def test_eq_default(Board):
    """A default board is equal to another instance of a default board."""
    assert Board() == Board()


def test_eq_modified(Board):
    """Two boards that have been modified identically are equal."""
    assert (Board().put('d4', Piece(Type.KNIGHT, Side.WHITE))
            == Board().put('d4', Piece(Type.KNIGHT, Side.WHITE)))


def test_eq_different_boards(board):
    """Two different boards are not equal."""
    assert board != board.put('h8', None)


def test_eq_other_type(board):
    """A board does not equal anything that is not a board."""
    assert board != 1
    assert board != 'Hello'
    assert board is not None
    assert board != []
    assert board != object()
    assert board != dict()


def test_from_fen(board, Board):
    """Board.from_fen correctly parses the default chess board."""
    assert board == Board.from_fen(
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')


def test_repr_from_fen(board, Board):
    """The output of Board.__repr__ can be forwarded to Board.from_fen to
    create an identical object.
    """
    assert Board.from_fen(repr(board)) == board


def test_from_fen_wrong_input(Board):
    """Board.from_fen raises a ValueError when the input is wrong."""
    with pytest.raises(ValueError):
        Board.from_fen('Hello, world!')
    with pytest.raises(ValueError):
        Board.from_fen('xxxxxxxx/8/8/8/8/8/8/8')
    with pytest.raises(ValueError):
        Board.from_fen('7/8/8/8/8/8/8/8')
    with pytest.raises(ValueError):
        Board.from_fen('p7/8')


def test_pretty(board):
    """Output a correct board."""
    assert board.pretty() == (
        '  A B C D E F G H\n'
        '8 r n b q k b n r\n'
        '7 p p p p p p p p\n'
        '6 . . . . . . . .\n'
        '5 . . . . . . . .\n'
        '4 . . . . . . . .\n'
        '3 . . . . . . . .\n'
        '2 P P P P P P P P\n'
        '1 R N B Q K B N R'
    )
