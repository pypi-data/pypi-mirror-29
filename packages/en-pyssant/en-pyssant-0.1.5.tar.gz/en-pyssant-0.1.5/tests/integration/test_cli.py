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

"""Tests for the command line interface.

.. NOTE::
    These are tests against a _PRIVATE INTERFACE_.  They can fail when the
    implementation changes.
"""

# pylint: disable=no-self-use,invalid-name,redefined-outer-name

from unittest import mock

from en_pyssant import _cli


def patch_input(monkeypatch, value):
    """Patch the input method in _cli to return *value*."""
    monkeypatch.setattr('en_pyssant._cli.input', lambda *args: value)


def test_prompt_play_again_yes(monkeypatch):
    """Test for inputs that equate to 'yes'."""
    for value in ['y', 'Y']:
        patch_input(monkeypatch, value)
        assert _cli.prompt_play_again()


def test_prompt_play_again_no(monkeypatch):
    """Test for inputs that equate to 'no'."""
    for value in ['n', 'N', 'whatever', '']:
        patch_input(monkeypatch, value)
        assert not _cli.prompt_play_again()


def test_prompt_player_count_singleplayer(monkeypatch):
    """1 is singleplayer."""
    patch_input(monkeypatch, '1')
    assert _cli.prompt_player_count() == 1


def test_prompt_player_count_multiplayer(monkeypatch):
    """2 is multiplayer."""
    patch_input(monkeypatch, '2')
    assert _cli.prompt_player_count() == 2


def test_prompt_player_count_neither(monkeypatch):
    """Test against invalid inputs."""
    mock_func = mock.create_autospec(input)
    mock_func.side_effect = ['3', '0', '', 'whatever', '1']
    monkeypatch.setattr('en_pyssant._cli.input', mock_func)
    assert _cli.prompt_player_count() == 1
    assert mock_func.call_count == 5
