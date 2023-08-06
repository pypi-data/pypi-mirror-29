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

"""The central game object."""

import re
import textwrap
from collections import OrderedDict
from io import StringIO
from multiprocessing import RLock
from typing import (Iterable, Iterator, Optional, Sequence, TextIO, Tuple,
                    Type, Union)

from . import rules
from ._board import Board, DictBoard
from ._core import HistoryRecord, Move, Side, Square
from ._position import Position

TAG_PAIR_PATTERN = re.compile(
    r'\[(.*?)\s"(.*?)"\]')
MOVE_NUMBER_PATTERN = re.compile(
    r'\d+\.')


def tag_pair(name: str, value: str) -> str:
    """Return a formatted string of a tag pair for PGN."""
    return '[{} "{}"]\n'.format(name, value)


def match_tag_pair(text: str) -> Optional[Tuple[str, str]]:
    """Extract the tag pair values from *text*.  *text* must be a single-line
    string.

    The tuple that is returned is (name, value).
    """
    match = TAG_PAIR_PATTERN.match(text)
    if match:
        return match.groups()
    return None


def parse_tag_pairs(text: str, game) -> None:
    """Read all tag pairs from *text* and add them to the metadata of *game*.
    """
    for line in text.splitlines():
        result = match_tag_pair(line)
        if result:
            if result[0] == 'Result':
                continue
            game.metadata[result[0]] = result[1]


def read_until(text: TextIO, match: Iterable[str]) -> str:
    """Read from *text* until (and including) a character from *match*."""
    results = []
    while True:
        result = text.read(1)
        results.append(result)
        if result in match:
            break
        if not result:
            break
    return ''.join(results)


class Game:
    """Central game object that is used to play the game.

    All undocumented methods are documented in :mod:`~en_pyssant.rules`.
    Except where :mod:`~en_pyssant.rules` accepts *position* and *history*
    parameters, those parameters are implicit in this class.  The instance
    variables are passed and altered.

    :ivar position: Chess position.
    :vartype position: :class:`Position`
    :ivar history: History of plays.
    :ivar ruleset: Game ruleset.
    :ivar metadata: Ordered dictionary of game metadata.
    :ivar lock: A lock for accessing/modifying instance variables.
    :vartype lock: :class:`multiprocessing.RLock`
    """
    # pylint: disable=missing-docstring,too-many-arguments

    def __init__(
            self,
            position: Position = None,
            history: Sequence[HistoryRecord] = None,
            ruleset=None,
            event: str = None,
            site: str = None,
            date: str = None,
            round: str = None,
            white: str = None,
            black: str = None):
        """:param position: Chess position.
        :param history: History of plays.
        :param ruleset: Game ruleset.
        :param event: The name of the tournament or match event.
        :param site: The location of the event.
        :param date: The starting date of the game.
        :param round: The playing round ordinal of the game.
        :param white: The player of the white pieces.
        :param black: The player of the black pieces.
        """
        if position is None:
            position = Position()
        if history is None:
            history = tuple()
        if ruleset is None:
            ruleset = rules

        self.position = position
        self.history = tuple(history)
        self.ruleset = ruleset
        self.metadata = OrderedDict()

        if event:
            self.metadata['Event'] = event
        if site:
            self.metadata['Site'] = site
        if date:
            self.metadata['Date'] = date
        if round:
            self.metadata['Round'] = round
        if white:
            self.metadata['White'] = white
        if black:
            self.metadata['Black'] = black

        self.lock = RLock()

    @classmethod
    def from_pgn(
            cls,
            pgn: str,
            board_cls: Type[Board] = DictBoard,
            ruleset=None) -> 'Game':
        """Generate a :class:`Game` from a Portable Game Notation string.

        An example PGN is::

            [Event "F/S Return Match"]
            [Site "Belgrade, Serbia JUG"]
            [Date "1992.11.04"]
            [Round "29"]
            [White "Fischer, Robert J."]
            [Black "Spassky, Boris V."]
            [Result "1/2-1/2"]

            1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5
            7. Bb3 d6 8. c3 O-O 9. h3 Nb8 10. d4 Nbd7 11. c4 c6 12. cxb5 axb5
            13. Nc3 Bb7 14. Bg5 b4 15.  Nb1 h6 16. Bh4 c5 17. dxe5 Nxe4
            18. Bxe7 Qxe7 19. exd6 Qf6 20. Nbd2 Nxd6 21.  Nc4 Nxc4 22. Bxc4 Nb6
            23. Ne5 Rae8 24. Bxf7+ Rxf7 25. Nxf7 Rxe1+ 26. Qxe1 Kxf7 27. Qe3
            Qg5 28. Qxg5 hxg5 29. b3 Ke6 30. a3 Kd6 31. axb4 cxb4 32. Ra5 Nd5
            33.  f3 Bc8 34. Kf2 Bf5 35. Ra7 g6 36. Ra6+ Kc5 37. Ke1 Nf4 38. g3
            Nxh3 39. Kd2 Kb5 40. Rd6 Kc5 41. Ra6 Nf2 42. g4 Bd3 43. Re6 1/2-1/2


        :param pgn: Portable Game Notation.
        :param board_cls: Type that will be used for the board representation.
        :param ruleset: Game ruleset.
        :return: A game.
        :raise ValueError: Input is invalid.
        """
        position = Position(board=board_cls())
        game = Game(position=position, ruleset=ruleset)
        parse_tag_pairs(pgn, game)

        pgn = '\n'.join([
            line for line in pgn.splitlines()
            if not line.startswith(';')
            and not line.startswith('[')])

        text = StringIO(pgn)

        while True:
            single = read_until(text, [' ', '\n'])
            if not single:
                break
            single = single.strip()
            if not single:
                continue
            if single.startswith('('):
                if ')' not in single:
                    read_until(text, [')'])
                continue
            single = single.rstrip('!?')
            if single.startswith('$'):
                continue
            if MOVE_NUMBER_PATTERN.match(single):
                continue
            if single in ['1-0', '0-1', '*', '1/2-1/2']:
                continue
            # single should now be a move
            try:
                game.do_move(single)
            except ValueError:
                raise

        return game

    def _result(self):
        """Create a string for the Result PGN tag."""
        if self.is_draw():
            return '1/2-1/2'
        winner = self.winner()
        if winner == Side.WHITE:
            return '1-0'
        elif winner == Side.BLACK:
            return '0-1'
        return '*'

    def pgn(self) -> str:
        """Generate and return the Portable Game Notation.

        The movetext is wrapped at 80 characters.

        :return: Portable Game Notation of current game state.
        """
        tag_pairs = StringIO()
        movetext = StringIO()

        with self.lock:
            for key, value in self.metadata.items():
                tag_pairs.write(tag_pair(key, value))
            tag_pairs.write(tag_pair('Result', self._result()))

            for i, record in enumerate(self.history):
                # Even moves are white moves
                if not i % 2:
                    movetext.write('{}. '.format(int(i / 2) + 1))
                movetext.write(record.move.san(record.position, self.ruleset))
                movetext.write(' ')
            if self.is_gameover():
                movetext.write(self._result())

        return '\n'.join(
            [tag_pairs.getvalue()]
            + textwrap.wrap(movetext.getvalue().strip(), width=80))

    def attacked(self, side: Side, square: Square) -> bool:
        with self.lock:
            return self.ruleset.attacked(self.position, side, square)

    def moves(self) -> Iterator[Move]:
        with self.lock:
            return self.ruleset.moves(self.position)

    def do_move(self, move: Union[Move, str], force: bool = False) -> Position:
        """
        .. IMPORTANT::
            :attr:`position` and :attr:`history` are updated when calling this
            method.
        """
        with self.lock:
            if isinstance(move, str):
                move = Move.from_san(move, self.position, self.ruleset)
            elif not force:
                move = move.expand(self.position, self.ruleset)

            record = HistoryRecord(self.position, move)
            # We expanded the move here, so force=True.
            new_position = self.ruleset.do_move(
                self.position, move, force=True)

            self.position = new_position
            self.history += (record,)

            return new_position

    def is_check(self, side: Side = None) -> bool:
        with self.lock:
            return self.ruleset.is_check(self.position, side=side)

    def is_stale(self) -> bool:
        with self.lock:
            return self.ruleset.is_stale(self.position)

    def is_checkmate(self) -> bool:
        with self.lock:
            return self.ruleset.is_checkmate(self.position)

    def is_stalemate(self) -> bool:
        with self.lock:
            return self.ruleset.is_stalemate(self.position)

    def is_fifty_move(self) -> bool:
        with self.lock:
            return self.ruleset.is_fifty_move(self.position)

    def is_insufficient_material(self) -> bool:
        with self.lock:
            return self.ruleset.is_insufficient_material(self.position)

    def is_threefold_repetition(self) -> bool:
        with self.lock:
            return self.ruleset.is_threefold_repetition(history=self.history)

    def is_draw(self) -> bool:
        with self.lock:
            return self.ruleset.is_draw(self.position, history=self.history)

    def is_gameover(self) -> bool:
        with self.lock:
            return self.ruleset.is_gameover(
                self.position, history=self.history)

    def winner(self) -> Side:
        with self.lock:
            return self.ruleset.winner(self.position)

    def loser(self) -> Side:
        with self.lock:
            return self.ruleset.loser(self.position)
