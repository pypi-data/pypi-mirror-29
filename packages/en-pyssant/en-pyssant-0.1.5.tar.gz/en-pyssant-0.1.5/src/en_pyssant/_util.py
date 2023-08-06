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

"""Miscellaneous utility functions and the like."""

import re
from functools import lru_cache
from typing import List

from ._core import Side, Square


@lru_cache(maxsize=2)
def opponent(side: Side) -> Side:
    """Return the opposite side.

    >>> opponent(Side.WHITE) == Side.BLACK
    True

    :param side: Proponent side.
    """
    return Side(not side.value)


def validate_fen_board(fen: str) -> bool:
    """Check whether the board portion of a given Forsyth-Edwards Notation is
    valid.

    :param fen: Board portion of Forsyth-Edwards Notation.
    :return: Whether *fen* is valid.
    """
    fen = fen.split()[0]
    chunks = fen.split('/')
    file_length = len(chunks)

    if file_length != 8:
        return False

    for chunk in chunks:
        rank_length = 0
        for char in chunk:
            if char.isnumeric() and char != '0':
                rank_length += int(char)
            elif char.lower() in 'kqrbnp':
                rank_length += 1
            else:
                return False
        if rank_length != 8:
            return False

    return True


def validate_fen(fen: str) -> bool:
    """Check whether a given Forsyth-Edwards Notation is valid

    :param fen: Forsyth-Edwards Notation.
    :return: Whether *fen* is valid.
    """
    # pylint: disable=too-many-return-statements
    parts = fen.split()

    if len(parts) != 6:
        return False

    if not validate_fen_board(parts[0]):
        return False

    if parts[1] not in 'wb':
        return False

    if not re.match('^K?Q?k?q?$', parts[2]) and parts[2] != '-':
        return False

    if parts[3] != '-' and parts[3] not in ALL_SQUARES:
        return False

    try:
        half_move_clock = int(parts[4])
        move_count = int(parts[5])
    except ValueError:
        return False

    if half_move_clock < 0 or move_count < 1:
        return False

    return True


def _all_squares() -> List[Square]:
    """Return a list of all squares from a8 to h1.  Increment files before
    ranks.
    """
    squares = []
    for i in reversed(range(1, 9)):
        for char in 'abcdefgh':
            squares.append(Square('{}{}'.format(char, i)))
    return squares


ALL_SQUARES = _all_squares()
