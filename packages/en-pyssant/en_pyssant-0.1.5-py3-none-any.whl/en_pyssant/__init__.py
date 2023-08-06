# -*- coding: utf-8 -*-
#
# Copyright (C) 2017  Carmen Bianca Bakker <carmen@carmenbianca.eu>
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

"""En Pyssant is a chess implementation and engine."""

from ._board import Board, BytesBoard, DictBoard, ListBoard, StringBoard
from ._core import (Direction, Gameover, HistoryRecord, Move, MoveFlag, Piece,
                    Side, Square, Type)
from ._game import Game
from ._position import CastlingAvailability, Position

__all__ = [
    'Type',
    'Side',
    'Piece',
    'Direction',
    'Square',
    'MoveFlag',
    'Move',
    'HistoryRecord',
    'Gameover',
    'CastlingAvailability',
    'Board',
    'BytesBoard',
    'DictBoard',
    'ListBoard',
    'StringBoard',
    'Position',
    'Game',
]

__author__ = 'Carmen Bianca Bakker'
__email__ = 'carmen@carmenbianca.eu'
__license__ = 'GPL-3.0+'
__version__ = '0.1.5'
