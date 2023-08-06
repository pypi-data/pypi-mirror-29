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

"""Benchmark suite for En Pyssant."""

import pytest

from en_pyssant import Move, Piece, Side, Type, rules
from en_pyssant._util import ALL_SQUARES
from en_pyssant.rules import attacked, moves

pytestmark = pytest.mark.benchmark  # pylint: disable=invalid-name


@pytest.mark.benchmark(group='board_read')
def test_read_all_board(benchmark, board):
    """Benchmark how long it takes to read all squares on the board."""
    squares = ALL_SQUARES

    def read_all(board):
        """Read all squares on the board."""
        return [board[square] for square in squares]

    benchmark(read_all, board)


@pytest.mark.benchmark(group='board_write')
def test_clear_board(benchmark, board):
    """Benchmark how long it takes to clear all squares on the board."""
    squares = ALL_SQUARES

    def clear(board):
        """Clear the board."""
        for square in squares:
            board = board.put(square, None)
        return board

    benchmark(clear, board)


@pytest.mark.benchmark(group='board_write')
def test_fill_board(benchmark, board):
    """Benchmark how long it takes to fill the board with pawns."""
    squares = ALL_SQUARES
    pawn = Piece(Type.PAWN, Side.WHITE)

    def fill(board):
        """Fill the board."""
        for square in squares:
            board = board.put(square, pawn)
        return board

    benchmark(fill, board)


@pytest.mark.benchmark(group='moves')
def test_moves(benchmark, position_multi_board):
    """Benchmark :func:`moves` on the default position."""
    def all_moves(position_multi_board):
        """Exhaust the generator."""
        return list(moves(position_multi_board))
    benchmark(all_moves, position_multi_board)


@pytest.mark.benchmark(group='attacked')
def test_attacked(benchmark, position_multi_board):
    """Benchmark :func:`attacked` on the default position."""
    benchmark(attacked, position_multi_board, Side.WHITE, 'd4')


@pytest.mark.benchmark(group='san')
def test_san(benchmark, san_position_multi_board):
    """Benchmark :meth:`Move.san`."""
    move = Move('c2', 'c7')
    move = move.expand(san_position_multi_board, rules)

    def san(san_position_multi_board):
        """Get san of move."""
        move.san(san_position_multi_board, rules)

    benchmark(san, san_position_multi_board)


@pytest.mark.benchmark(group='from_san')
def test_from_san(benchmark, san_position_multi_board):
    """Benchmark :meth:`Move.from_san`."""
    san = 'Rxc7+'

    def from_san(san_position_multi_board):
        """Create Move from san."""
        Move.from_san(san, san_position_multi_board, rules)

    benchmark(from_san, san_position_multi_board)
