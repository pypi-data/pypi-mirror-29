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

"""Various chess engines."""

import random
from abc import ABCMeta, abstractmethod
from multiprocessing import Event

from ._core import Move
from ._game import Game


class Engine(metaclass=ABCMeta):
    """Abstract base class for engine implementations."""

    @abstractmethod
    def think_for(self, seconds: float) -> None:
        """Perform analysis of the board for a _maximum_ of *seconds*.  It is
        perfectly permissible that this function blocks for a lower amount of
        time.

        If *seconds* is 0, block forever until :meth:`stop_thinking` is called.

        :param seconds: Amount of seconds to process.
        """

    @abstractmethod
    def stop_thinking(self) -> None:
        """Stop the loop in :meth:`think_for`.  This method blocks until the
        loop is stopped.
        """

    @abstractmethod
    def best_move(self) -> Move:
        """Return the move that the engine thinks is best.  This probably
        requires some processing in advance with :meth:`think_for`.

        :return: The best move.
        """


class RandomEngine(Engine):
    """An Engine implementation that returns random moves.  The purpose of this
    engine is solely to prototype.
    """

    def __init__(self, game: Game) -> None:
        self._game = game
        self._random = random.SystemRandom()
        self._stop_event = Event()
        self._stopped_event = Event()

    def think_for(self, seconds: float) -> None:
        if seconds == 0:
            self._stop_event.wait()
            self._stop_event.clear()
            self._stopped_event.set()

    def stop_thinking(self) -> None:
        self._stop_event.set()
        self._stopped_event.wait()
        self._stopped_event.clear()

    def best_move(self) -> Move:
        moves = self._game.moves()
        return self._random.choice(list(moves))
