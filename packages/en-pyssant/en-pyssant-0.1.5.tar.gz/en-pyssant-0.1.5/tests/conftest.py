# -*- coding: utf-8 -*-
#
# Copyright (C) 2017  Carmen Bianca Bakker <carmen@carmenbianca.eu>
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

"""Global fixtures and configuration."""

# pylint: disable=invalid-name,redefined-outer-name

import sys
from collections import namedtuple
from unittest import mock

import pytest

from en_pyssant import CastlingAvailability, DictBoard, Game, Position, Side
from en_pyssant._board import all_board_classes


@pytest.fixture(params=all_board_classes())
def Board(request):
    """Yield the available Board classes."""
    yield request.param


@pytest.fixture
def board(Board):
    """Return a default Board."""
    return Board()


@pytest.fixture
def position_multi_board(board):
    """Yield a default Position with any Board."""
    return Position(board=board)


@pytest.fixture
def position():
    """Return a default Position."""
    return Position()


@pytest.fixture
def san_position(b):
    """Return the fixture used for SAN tests."""
    return Position(
        board=b.SAN_BOARD,
        castling={
            Side.WHITE: CastlingAvailability(False, False),
            Side.BLACK: CastlingAvailability(False, False),
        },
    )


@pytest.fixture
def san_position_multi_board(san_position, Board):
    """Return the fixture used for SAN tests, with any Board."""
    return Position.from_fen(repr(san_position), board_cls=Board)


@pytest.fixture
def mock_rules():
    """Return a mocked spec of en_pyssant.rules."""
    from en_pyssant import rules
    return mock.Mock(spec=rules)


@pytest.fixture
def mocked_game(mock_rules):
    """Return a Game object with a mocked ruleset."""
    return Game(ruleset=mock_rules)


def create_board(Board, string):
    """Create a :class:`Board` from a string formatted as such::

        'rnbqkbnr'  # a8-h8
        'pppppppp'  # a7-h7
        '        '  # a6-h6
        '        '  # a5-h6
        '        '  # a4-h4
        '        '  # a3-h3
        'PPPPPPPP'  # a2-h2
        'RNBQKBNR'  # a1-h1

    The logic is basically copied from Board.__repr__.
    """
    assert len(string) == 64
    chunks = zip(*[iter(string)] * 8)  # Split into 8 chunks of 8
    fen_chunks = []

    for chunk in chunks:
        fen_chunk = []
        counter = 0

        for char in chunk:
            if not char.isspace():
                if counter:
                    fen_chunk.append(str(counter))
                    counter = 0
                fen_chunk.append(char)
            else:
                counter += 1
        if counter:
            fen_chunk.append(str(counter))

        fen_chunks.append(''.join(fen_chunk))

    fen_string = '/'.join(fen_chunks)
    return Board.from_fen(fen_string)


BOARDS = {
    'INITIAL_BOARD': (
        'rnbqkbnr'  # a8-h8
        'pppppppp'  # a7-h7
        '        '  # a6-h6
        '        '  # a5-h5
        '        '  # a4-h4
        '        '  # a3-h3
        'PPPPPPPP'  # a2-h2
        'RNBQKBNR'  # a1-h1
    ),

    'EN_PASSANT_BOARD': (
        'rnbqkbnr'  # a8-h8
        'p ppp p '  # a7-h7
        '        '  # a6-h6
        '     pPp'  # a5-h5
        'PpP     '  # a4-h4
        '        '  # a3-h3
        ' P PPP P'  # a2-h2
        'RNBQKBNR'  # a1-h1
    ),

    'KING_ROOK_BOARD': (
        '        '  # a8-h8
        ' k      '  # a7-h7
        '        '  # a6-h6
        '        '  # a5-h5
        '        '  # a4-h4
        ' R      '  # a3-h3
        '        '  # a2-h2
        '        '  # a1-h1
    ),

    'SAN_BOARD': (
        '        '  # a8-h8
        'k p  B P'  # a7-h7
        '      p '  # a6-h6
        '     B B'  # a5-h5
        '        '  # a4-h4
        ' R      '  # a3-h3
        'n R     '  # a2-h2
        '    K   '  # a1-h1
    ),

    'CASTLEMATE_BOARD': (
        '     k  '  # a8-h8
        '        '  # a7-h7
        '        '  # a6-h6
        '        '  # a5-h5
        '        '  # a4-h4
        '        '  # a3-h3
        '    R R '  # a2-h2
        'R   K  R'  # a1-h1
    ),

    'QUEEN_BISHOP_BOARD': (
        '        '  # a8-h8
        '        '  # a7-h7
        '  q     '  # a6-h6
        '        '  # a5-h5
        '        '  # a4-h4
        '     B  '  # a3-h3
        '  P     '  # a2-h2
        '        '  # a1-h1
    ),

    'KNIGHT_BOARD': (
        '        '  # a8-h8
        ' ppp    '  # a7-h7
        ' pNp    '  # a6-h6
        ' ppp    '  # a5-h5
        '        '  # a4-h4
        '        '  # a3-h3
        '        '  # a2-h2
        '        '  # a1-h1
    ),

    'CASTLING_BOARD': (
        'r   k  r'  # a8-h8
        '        '  # a7-h7
        '        '  # a6-h6
        '        '  # a5-h5
        '        '  # a4-h4
        '        '  # a3-h3
        '        '  # a2-h2
        'R   K  R'  # a1-h1
    ),

    'STALEMATE_BOARD': (
        '        '  # a8-h8
        '        '  # a7-h7
        '        '  # a6-h6
        '        '  # a5-h5
        '        '  # a4-h4
        '   r r  '  # a3-h3
        '       r'  # a2-h2
        '    K   '  # a1-h1
    ),

    'CHECKMATE_BOARD': (
        '    k   '  # a8-h8
        '        '  # a7-h7
        '        '  # a6-h6
        '        '  # a5-h5
        '        '  # a4-h4
        '   rqr  '  # a3-h3
        '       r'  # a2-h2
        '    K   '  # a1-h1
    ),

    'PAWN_BOARD': (
        '        '  # a8-h8
        '        '  # a7-h7
        '        '  # a6-h6
        '        '  # a5-h5
        '        '  # a4-h4
        '        '  # a3-h3
        'P       '  # a2-h2
        '        '  # a1-h1
    ),

    'PROMOTION_BOARD': (
        '        '  # a8-h8
        'P       '  # a7-h7
        '        '  # a6-h6
        '        '  # a5-h5
        '        '  # a4-h4
        '        '  # a3-h3
        '        '  # a2-h2
        '        '  # a1-h1
    ),

    'KING_V_KING': (
        '    k   '  # a8-h8
        '        '  # a7-h7
        '        '  # a6-h6
        '        '  # a5-h5
        '        '  # a4-h4
        '        '  # a3-h3
        '        '  # a2-h2
        '    K   '  # a1-h1
    ),

    'KING_KNIGHT_V_KING': (
        '    k   '  # a8-h8
        '        '  # a7-h7
        '        '  # a6-h6
        '        '  # a5-h5
        '        '  # a4-h4
        '        '  # a3-h3
        '        '  # a2-h2
        '    K N '  # a1-h1
    ),

    'KING_BISHOP_V_KING_BISHOP': (
        '        '  # a8-h8
        '   bkb  '  # a7-h7
        '        '  # a6-h6
        '        '  # a5-h5
        '        '  # a4-h4
        '        '  # a3-h3
        '        '  # a2-h2
        '   BKB  '  # a1-h1
    ),
}


@pytest.fixture
def b():
    """Return a namedtuple of all boards in BOARDS."""
    B = namedtuple('B', BOARDS.keys())
    boards = {name: create_board(DictBoard, board)
              for name, board in BOARDS.items()}
    return B(**boards)


def pytest_configure(config):
    """Turn off exception details for Python 2."""
    if sys.version_info < (3,):
        config.addinivalue_line('doctest_optionflags',
                                'IGNORE_EXCEPTION_DETAIL')
