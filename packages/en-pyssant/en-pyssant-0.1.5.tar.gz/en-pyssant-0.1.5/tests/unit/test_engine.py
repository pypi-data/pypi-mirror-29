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

"""Unit tests for the chess engine implementations."""

# pylint: disable=no-self-use,invalid-name,redefined-outer-name

import threading
import time
from unittest import mock

import pytest

from en_pyssant import Game
from en_pyssant.engine import RandomEngine


@pytest.fixture(params=[RandomEngine])
def Engine(request):
    """Yield the available Engine classes."""
    yield request.param


@pytest.fixture
def engine(Engine):
    """Return a default engine with a mocked game."""
    game = mock.Mock(spec=Game)
    return Engine(game)


def test_think_for_less_than(engine):
    """:meth:`Engine.think_for` takes less than the passed amount of seconds.
    """
    # pylint: disable=unused-argument
    seconds = 0.5
    start = time.clock()
    engine.think_for(seconds)
    end = time.clock()
    assert end - start < seconds


def test_stop_thinking(engine):
    """:meth:`Engine.stop_thinking` stops an infinite thinking loop."""
    thread = threading.Thread(target=engine.think_for, args=(0,))
    thread.start()
    engine.stop_thinking()
    thread.join()
