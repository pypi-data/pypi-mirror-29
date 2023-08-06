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

"""Integrated tests for Game."""

# pylint: disable=invalid-name,redefined-outer-name,unused-variable

from unittest import mock

import pytest

from en_pyssant import Game, HistoryRecord, Side


def side_effect(*args, **kwargs):
    """Directly return arguments as a tuple."""
    return args, kwargs


def test_pgn_header():
    """The header of the PGN is correct."""
    game = Game(event='a', site='b', date='c', round='d', white='e', black='f')

    # Do a random move to separate the header from the moves in the PGN output.
    move = next(game.moves())
    game.do_move(move)

    header = game.pgn().split('\n\n')[0]

    assert header.split('\n\n')[0] == (
        '[Event "a"]\n'
        '[Site "b"]\n'
        '[Date "c"]\n'
        '[Round "d"]\n'
        '[White "e"]\n'
        '[Black "f"]\n'
        '[Result "*"]')


def test_pgn_fools_mate():
    """Play an entire game of Fool's Mate.  Check if its PGN is correct."""
    game = Game()
    moves = ['f3', 'e5', 'g4', 'Qh4#']

    for move in moves:
        game.do_move(move)

    pgn = game.pgn()
    header, movetext = pgn.split('\n\n')

    assert '[Result "0-1"]' in header
    assert movetext == (
        '1. f3 e5 2. g4 Qh4# 0-1')


def test_pgn_wraps():
    """Play a semi-long game.  Check if the PGN output wraps at 80 characters.
    """
    game = Game()
    moves = ['Na3', 'Na6', 'Nb1', 'Nb8']

    for i in range(4):
        for move in moves:
            game.do_move(move)

    movetext = game.pgn().split('\n\n')[1]

    assert movetext == (
        '1. Na3 Na6 2. Nb1 Nb8 3. Na3 Na6 4. Nb1 Nb8 5. Na3 Na6 6. Nb1 Nb8 7. '
        'Na3 Na6 8.\nNb1 Nb8')


def test_from_pgn_fools_mate():
    """Can read a simple PGN of a game of Fool's Mate."""
    pgn = (
        '[Date "2018-02-23"]\n'
        '[Result "0-1"]\n'
        '; This is a comment.\n'
        '(and this)\n'
        '\n'
        '1. f3 e5 2. g4 (this is another comment) Qh4# 0-1')

    game = Game.from_pgn(pgn)
    assert len(game.history) == 4
    assert game.metadata['Date'] == '2018-02-23'
    assert game.winner() == Side.BLACK


def test_pgn_self_compliant():
    """Can feed Game.pgn into Game.from_pgn and get the same output."""
    game = Game(date='2018-02-23')
    game.do_move('a3')

    pgn = game.pgn()
    new_game = Game.from_pgn(pgn)
    assert new_game.pgn() == pgn


def test_from_pgn_spec():
    """Can create a Game object from the sample PGN from the spec."""
    pgn = (
        '[Event "F/S Return Match"]\n'
        '[Site "Belgrade, Serbia JUG"]\n'
        '[Date "1992.11.04"]\n'
        '[Round "29"]\n'
        '[White "Fischer, Robert J."]\n'
        '[Black "Spassky, Boris V."]\n'
        '[Result "1/2-1/2"]\n'
        '\n'
        '1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5\n'
        '7. Bb3 d6 8. c3 O-O 9. h3 Nb8 10. d4 Nbd7 11. c4 c6 12. cxb5 axb5\n'
        '13. Nc3 Bb7 14. Bg5 b4 15.  Nb1 h6 16. Bh4 c5 17. dxe5 Nxe4\n'
        '18. Bxe7 Qxe7 19. exd6 Qf6 20. Nbd2 Nxd6 21.  Nc4 Nxc4 22. Bxc4 Nb6\n'
        '23. Ne5 Rae8 24. Bxf7+ Rxf7 25. Nxf7 Rxe1+ 26. Qxe1 Kxf7 27. Qe3\n'
        'Qg5 28. Qxg5 hxg5 29. b3 Ke6 30. a3 Kd6 31. axb4 cxb4 32. Ra5 Nd5\n'
        '33.  f3 Bc8 34. Kf2 Bf5 35. Ra7 g6 36. Ra6+ Kc5 37. Ke1 Nf4 38. g3\n'
        'Nxh3 39. Kd2 Kb5 40. Rd6 Kc5 41. Ra6 Nf2 42. g4 Bd3 43. Re6\n'
        '1/2-1/2\n')

    Game.from_pgn(pgn)


def test_attacked(mocked_game):
    """attacked is a correct facade method."""
    mocked_game.ruleset.attacked = mock.Mock(side_effect=side_effect)
    args, kwargs = mocked_game.attacked(1, 2)
    assert args == (mocked_game.position, 1, 2)


def test_moves(mocked_game):
    """moves is a correct facade method."""
    mocked_game.ruleset.moves = mock.Mock(side_effect=side_effect)
    args, kwargs = mocked_game.moves()
    assert args == (mocked_game.position,)


def test_do_move_force(mocked_game):
    """When do_move is called with force, the following things are true:

    - move is returned as-is.

    - The history is updated correctly.

    - The new position is the output of do_move.
    """
    mocked_game.ruleset.do_move = mock.Mock(side_effect=side_effect)
    starting_position = mocked_game.position
    position = mocked_game.do_move(1, force=True)
    assert position == mocked_game.position
    move = mocked_game.history[0].move
    assert move == 1
    args, kwargs = mocked_game.position
    assert args == (starting_position, move)
    assert kwargs == {'force': True}
    assert mocked_game.history == (HistoryRecord(starting_position, move),)


@pytest.mark.xfail
def test_do_move_no_force(monkeypatch, mocked_game):
    """When do_move is called without force, the following things are true:

    - move is returned expanded.

    - The history is updated correctly.

    - The new position is the output of do_move.
    """
    mock_expand_move = mock.Mock(side_effect=side_effect)
    monkeypatch.setattr('en_pyssant._game.Move.expand', mock_expand_move)
    mocked_game.ruleset.do_move = mock.Mock(side_effect=side_effect)
    starting_position = mocked_game.position
    position = mocked_game.do_move(1, force=False)
    assert position == mocked_game.position
    move = mocked_game.history[0].move
    args, kwargs = move
    assert args == (mocked_game.ruleset.moves(mocked_game.position), 1)
    mock_expand_move.assert_called_with(*args)
    args, kwargs = mocked_game.position
    assert args == (starting_position, move)
    assert kwargs == {'force': True}
    assert mocked_game.history == (HistoryRecord(starting_position, move),)


def test_is_check(mocked_game):
    """is_check is a correct facade method."""
    mocked_game.ruleset.is_check = mock.Mock(side_effect=side_effect)
    args, kwargs = mocked_game.is_check(side=1)
    assert args == (mocked_game.position,)
    assert kwargs == {'side': 1}


def test_is_stale(mocked_game):
    """is_stale is a correct facade method."""
    mocked_game.ruleset.is_stale = mock.Mock(side_effect=side_effect)
    args, kwargs = mocked_game.is_stale()
    assert args == (mocked_game.position,)


def test_is_checkmate(mocked_game):
    """is_checkmate is a correct facade method."""
    mocked_game.ruleset.is_checkmate = mock.Mock(side_effect=side_effect)
    args, kwargs = mocked_game.is_checkmate()
    assert args == (mocked_game.position,)


def test_is_stalemate(mocked_game):
    """is_stalemate is a correct facade method."""
    mocked_game.ruleset.is_stalemate = mock.Mock(side_effect=side_effect)
    args, kwargs = mocked_game.is_stalemate()
    assert args == (mocked_game.position,)


def test_is_fifty_move(mocked_game):
    """is_fifty_move is a correct facade method."""
    mocked_game.ruleset.is_fifty_move = mock.Mock(side_effect=side_effect)
    args, kwargs = mocked_game.is_fifty_move()
    assert args == (mocked_game.position,)


def test_is_insufficient_material(mocked_game):
    """is_insufficient_material is a correct facade method."""
    mocked_game.ruleset.is_insufficient_material = mock.Mock(
        side_effect=side_effect)
    args, kwargs = mocked_game.is_insufficient_material()
    assert args == (mocked_game.position,)


def test_is_threefold_repetition(mocked_game):
    """is_threefold_repetition is a correct facade method."""
    mocked_game.ruleset.is_threefold_repetition = mock.Mock(
        side_effect=side_effect)
    args, kwargs = mocked_game.is_threefold_repetition()
    assert args == tuple()
    assert kwargs == {'history': mocked_game.history}


def test_is_draw(mocked_game):
    """is_draw is a correct facade method."""
    mocked_game.ruleset.is_draw = mock.Mock(side_effect=side_effect)
    args, kwargs = mocked_game.is_draw()
    assert args == (mocked_game.position,)
    assert kwargs == {'history': mocked_game.history}


def test_is_gameover(mocked_game):
    """is_gameover is a correct facade method."""
    mocked_game.ruleset.is_gameover = mock.Mock(side_effect=side_effect)
    args, kwargs = mocked_game.is_gameover()
    assert args == (mocked_game.position,)
    assert kwargs == {'history': mocked_game.history}


def test_winner(mocked_game):
    """winner is a correct facade method."""
    mocked_game.ruleset.winner = mock.Mock(side_effect=side_effect)
    args, kwargs = mocked_game.winner()
    assert args == (mocked_game.position,)


def test_loser(mocked_game):
    """loser is a correct facade method."""
    mocked_game.ruleset.loser = mock.Mock(side_effect=side_effect)
    args, kwargs = mocked_game.loser()
    assert args == (mocked_game.position,)
