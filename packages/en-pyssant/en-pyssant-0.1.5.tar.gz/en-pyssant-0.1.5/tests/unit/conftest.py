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

"""Fixtures for unit tests."""

# pylint: disable=invalid-name,redefined-outer-name

from unittest import mock

import pytest

from en_pyssant import Position


@pytest.fixture
def BoardMock():
    """A mock of the class Board."""
    result = mock.Mock()
    result.from_fen.return_value = result
    result.__repr__ = lambda x: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    return result


@pytest.fixture
def position(BoardMock):
    """Return a default position with mocked board."""
    return Position(board=BoardMock)
