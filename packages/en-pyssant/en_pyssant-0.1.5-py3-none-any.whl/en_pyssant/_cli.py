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

"""Simple command-line interface for En Pyssant."""

from builtins import input
from typing import Dict, Type

from ._core import Move, Side
from ._game import Game
from .engine import Engine, RandomEngine


class Player:
    """Human player."""
    # pylint: disable=too-few-public-methods

    def __init__(self, game: Game) -> None:
        self._game = game

    def prompt_move(self) -> Move:
        """Prompt move to player from stdin."""
        print('Enter your move.')
        while True:
            value = input()
            try:
                return Move.from_san(
                    value, self._game.position, self._game.ruleset)
            except ValueError:
                print('Please insert a legal SAN move.')


class Computer:
    """Computer player (AI)."""
    # pylint: disable=too-few-public-methods

    def __init__(
            self,
            game: Game,
            engine_cls: Type[Engine] = RandomEngine) -> None:
        self._game = game
        self._engine = engine_cls(game)

    def prompt_move(self) -> Move:
        """Get a move from the engine."""
        self._engine.think_for(2)
        return self._engine.best_move()


def prompt_play_again() -> bool:
    """Ask the player whether they would like to play again."""
    print('Do you want to play again? (y/N) ', end='')
    value = input()
    return value.lower() == 'y'


def prompt_player_count() -> int:
    """Ask the player whether they would like to play singleplayer or
    multiplayer.
    """
    while True:
        print('How many human players? (1/2) ', end='')
        value = input()
        if value == '1':
            return 1
        if value == '2':
            return 2
    return 0


def single_game(game: Game, players: Dict[Side, Player]) -> None:
    """Play a single game."""
    while True:
        print()
        print(game.position.pretty())
        print()
        if game.is_gameover():
            print('Game over!')
            break
        move = players[game.position.side_to_play].prompt_move()
        game.do_move(move)


def main() -> None:
    """Start the CLI game."""
    while True:
        player_count = prompt_player_count()
        game = Game()
        players = {
            Side.WHITE: Player(game),
        }

        if player_count < 2:
            players[Side.BLACK] = Computer(game)
        else:
            players[Side.BLACK] = Player(game)

        single_game(game, players)

        # Play again?
        if not prompt_play_again():
            break
