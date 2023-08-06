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

"""Unit tests for Square."""

import pytest

from en_pyssant import Direction, Side, Square
from en_pyssant._util import opponent


def test_all_valid_squares():
    """Can create all 64 valid squares.

    Also verify whether Square's properties work.
    """
    colour = Side.BLACK
    for i in range(1, 9):
        for j in 'abcdefgh':
            square = Square('{}{}'.format(j, i))
            assert square.rank == i
            assert square.file == j
            assert square.colour == colour
            colour = opponent(colour)
        colour = opponent(colour)


def test_invalid_squares():
    """Test some invalid arguments and verify that they raise an exception.
    """
    invalid_squares = [
        'a0',
        'a9',
        'A1',
        '`1',
        'i1',
        'hello world',
        '11',
        'aa',
        '',
        '1',
        'a',
        '1a',
        'a ',
        ' 1',
        'a1.0',
        'aa1',
    ]
    for square in invalid_squares:
        with pytest.raises(ValueError):
            Square(square)


def test_up_right_down_left():
    """Test if all directions return a correct new square."""
    square = Square('a1')
    squares = []

    squares.append(square.up())
    squares.append(squares[-1].right())
    squares.append(squares[-1].down())
    squares.append(squares[-1].left())

    seen = {square for square in squares}
    assert len(seen) == 4  # all squares unique
    assert square == squares[-1]  # end up where we started


def test_goto():
    """Test if goto returns the correct new square."""
    square = Square('d4')
    direction_destinations = [
        (Direction.UP, 'd5'),
        (Direction.DOWN, 'd3'),
        (Direction.LEFT, 'c4'),
        (Direction.RIGHT, 'e4'),
    ]
    for thing in direction_destinations:
        assert square.goto(thing[0]) == thing[1]


def test_correct_directions():
    """Test if the directions return the same as their goto equivalent."""
    square = Square('d4')
    assert square.goto(Direction.UP) == square.up()
    assert square.goto(Direction.RIGHT) == square.right()
    assert square.goto(Direction.DOWN) == square.down()
    assert square.goto(Direction.LEFT) == square.left()


def test_invalid_directions():
    """Test if the direction can't return a value outside of the board."""
    lower_left = Square('a1')
    upper_right = Square('h8')

    actions = [
        (lower_left, Direction.DOWN),
        (lower_left, Direction.LEFT),
        (upper_right, Direction.UP),
        (upper_right, Direction.RIGHT),
    ]

    for action in actions:
        with pytest.raises(IndexError):
            action[0].goto(action[1])


def test_traverse():
    """Test if traverse correctly traverses the board and ends up at the
    right destination.
    """
    square = Square('a1')
    ups = (Direction.UP,) * 7
    downs = (Direction.DOWN,) * 7
    section = ups + (Direction.RIGHT,) + downs + (Direction.RIGHT,)

    directions = section * 4
    directions = directions[:-1]

    square = square.traverse(directions)
    assert square == 'h1'
