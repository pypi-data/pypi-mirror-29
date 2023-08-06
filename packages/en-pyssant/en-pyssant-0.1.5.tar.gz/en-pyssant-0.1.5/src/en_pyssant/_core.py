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

"""Core functionality of En Pyssant.

Safe to assume that all submodules depend on this module.
"""

import re
from collections import namedtuple
from enum import Enum
from functools import lru_cache
from types import MethodType
from typing import Sequence, Set, Union


SAN_END_PATTERN = re.compile(
    r'[+#]?[?!]*$')
SAN_PATTERN = re.compile(
    r'([PNBRQK])?([a-h])?([1-8])?x?-?([a-h][1-8])([QRBN])?', re.IGNORECASE)


def stripped_san(san: str) -> str:
    """Remove superfluous symbols from *san*."""
    return re.sub(SAN_END_PATTERN, '', san)


class Type(Enum):
    """Type of piece."""
    KING = 'k'
    QUEEN = 'q'
    ROOK = 'r'
    BISHOP = 'b'
    KNIGHT = 'n'
    PAWN = 'p'


class Side(Enum):
    """Colours corresponding to sides."""
    WHITE = 1
    BLACK = 0


class Piece(namedtuple('Piece', ['type', 'side'])):
    """A chess piece.  This object is immutable.

    >>> white_rook = Piece(Type.ROOK, Side.WHITE)
    >>> white_rook.side = Side.BLACK
    Traceback (most recent call last):
        ...
    AttributeError: can't set attribute
    """
    __slots__ = ()

    # Cache this.  The object is immutable and there are only 2 * 6 possible
    # permutations of this object.  Powers of 2 are more efficient for
    # lru_cache so use 2**4.
    @lru_cache(maxsize=16)
    def __new__(cls, type: Type, side: Side) -> 'Piece':
        """:param type: Type of piece.
        :param side: Side to which the piece belongs.
        """
        return super().__new__(cls, type, side)

    def __str__(self):
        if self.side == Side.WHITE:
            return self.type.value.upper()
        return self.type.value.lower()


class Direction(Enum):
    """General four directions."""
    # (file, rank)
    UP = (0, 1)  # pylint: disable=invalid-name
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Square(str):
    """A wrapper class around :class:`str` that handles only chess squares.

    >>> Square('a1')
    'a1'
    >>> Square('')
    Traceback (most recent call last):
        ...
    ValueError: '' is not a valid square
    >>> Square('a9')
    Traceback (most recent call last):
        ...
    ValueError: 'a9' is not a valid square
    """

    @lru_cache(maxsize=64)
    def __new__(cls, string: str) -> 'Square':
        error = False
        if len(string) != 2:
            error = True
        elif not 'a' <= string[0] <= 'h' or not '1' <= string[1] <= '8':
            error = True
        if error:
            raise ValueError('{} is not a valid square'.format(repr(string)))
        square = super().__new__(cls, string)
        square.goto = lru_cache(maxsize=4)(MethodType(cls.goto, square))
        square.in_bounds = lru_cache(maxsize=128)(MethodType(cls.in_bounds,
                                                             square))
        return square

    @property
    def rank(self) -> int:
        """The rank (or row) of the square."""
        return int(self[1])

    @property
    def file(self) -> str:
        """The file (or column) of the square."""
        return self[0]

    @property
    def colour(self) -> Side:
        """Colour of the square."""
        return Side.WHITE if (ord(self.file) + self.rank) % 2 else Side.BLACK

    def goto(self, direction: Direction) -> 'Square':
        """:param direction: Direction to go to.
        :return: One square in the given direction.
        :raise IndexError: Destination out of bounds.
        """
        offset = direction.value
        try:
            return self.__class__('{}{}'.format(
                chr(ord(self.file) + offset[0]),
                self.rank + offset[1]
            ))
        except ValueError:
            raise IndexError('Cannot go to {} from {}'.format(direction.name,
                                                              repr(self)))

    def up(self) -> 'Square':  # pylint: disable=invalid-name
        """:return: One square up.
        :raise IndexError: Cannot go up.
        """
        return self.goto(Direction.UP)

    def down(self) -> 'Square':
        """:return: One square down.
        :raise IndexError: Cannot go down.
        """
        return self.goto(Direction.DOWN)

    def left(self) -> 'Square':
        """:return: One square to the left.
        :raise IndexError: Cannot go left.
        """
        return self.goto(Direction.LEFT)

    def right(self) -> 'Square':
        """:return: One square to the right.
        :raise IndexError: Cannot go right.
        """
        return self.goto(Direction.RIGHT)

    def traverse(self, path: Sequence[Direction]) -> 'Square':
        """:param path: Sequence of directions to follow.  Must be hashable.
        :return: The square at the end of the path.
        :raise IndexError: Path goes out of bounds.
        """
        destination = self.in_bounds(path)
        if destination:
            return destination
        raise IndexError('Cannot traverse {!r} from {!r}'.format(path, self))

    def in_bounds(self, path: Sequence[Direction]) -> Union['Square', bool]:
        """Traverse with *path*.  Return the destination if it is inside the
        bounds of a chess board.  Else, return :const:`False`.

        :param path: Path to traverse to destination.  Must be hashable.
        :return: Destination square or :const:`False`
        """
        balance = (0, 0)  # Total offset from origin.
        for direction in path:
            offset = direction.value
            balance = tuple(map(sum, zip(balance, offset)))
        file_ = chr(ord(self.file) + balance[0])
        rank = self.rank + balance[1]
        if 'a' <= file_ <= 'h' and rank in range(1, 9):
            return self.__class__('{}{}'.format(file_, rank))
        return False


class MoveFlag(Enum):
    """Flags associated with a move."""
    NON_CAPTURE = 0
    STANDARD_CAPTURE = 1
    EN_PASSANT_CAPTURE = 2
    PAWN_PUSH = 3
    QUEENSIDE_CASTLING = 4
    KINGSIDE_CASTLING = 5
    PROMOTION = 6


class Move(namedtuple('Move', ['origin', 'destination', 'piece', 'captured',
                               'promotion', 'flags'])):
    """A move on the chess board.

    Under normal circumstances, you only need to provide *origin*,
    *destination* and possibly *promotion* when using a Move object to
    interface with the rest of the API.  The rest is metadata, as it were.
    """
    __slots__ = ()

    # pylint: disable=too-many-arguments
    def __new__(
            cls,
            origin: Square,
            destination: Square,
            piece: Piece = None,
            captured: Piece = None,
            promotion: Type = None,
            flags: Set[MoveFlag] = None) -> 'Move':
        """:param origin: Square from which the piece has moved.
        :param destination: Square to which the piece has moved.
        :param piece: The piece that has moved.
        :param captured: If a capture move: Piece that has been captured.
        :param promotion: The piece type that the pawn has been promoted to.
        :param flags: Flags associated with move.
        """
        if not isinstance(origin, Square):
            origin = Square(origin)
        if not isinstance(destination, Square):
            destination = Square(destination)
        if flags is None:
            flags = set()
        return super().__new__(cls, origin, destination, piece, captured,
                               promotion, flags)

    def expand(self, position, ruleset) -> 'Move':
        """Given a move that contains only *origin* and *destination*, return a
        new, fully descriptive move that contains all fields.

        Promotion moves that do not already specify which piece to promoto to
        will default to queen promotions.

        :param position: Chess position before the move is performed.
        :type position: :class:`Position`
        :param ruleset: Game ruleset.
        :return: A fully expanded move.
        :raise ValueError: Move is invalid.
        """
        promotion = self.promotion
        if not promotion:
            promotion = Type.QUEEN

        for move in ruleset.moves(position):
            if (self.origin == move.origin
                    and self.destination == move.destination):
                # If we're dealing with a promotion, only return the promotion
                # that matches the promotion target.
                if MoveFlag.PROMOTION in move.flags:
                    if promotion == move.promotion:
                        return move
                else:
                    return move
        raise ValueError('{} is not a valid move'.format(repr(self)))

    def san(self, position, ruleset) -> str:
        """Return the Standard Algebraic Notation of a move.

        :param position: Chess position _before_ the move is performed.
        :type position: :class:`Position`
        :param ruleset: Game ruleset.
        :return: Standard Algebraic Notation.
        """
        result = ''

        if MoveFlag.KINGSIDE_CASTLING in self.flags:
            result = 'O-O'
        elif MoveFlag.QUEENSIDE_CASTLING in self.flags:
            result = 'O-O-O'
        else:
            if self.piece.type != Type.PAWN:
                disambiguator = self._disambiguate_san(position, ruleset)
                # TODO: Make following line nicer.
                piece = self.piece.type.value.upper()
                result += '{}{}'.format(piece, disambiguator)
            if self.captured:
                if self.piece.type == Type.PAWN:
                    result += self.origin.file
                result += 'x'
            result += self.destination
            if MoveFlag.PROMOTION in self.flags:
                result += self.promotion.value.upper()

        new_position = ruleset.do_move(position, self)
        if ruleset.is_check(new_position):
            if ruleset.is_stale(new_position):
                result += '#'
            else:
                result += '+'

        return result

    @classmethod
    def from_san(
            cls,
            san: str,
            position,
            ruleset,
            strict: bool = False) -> 'Move':
        """Return a :class:`Move` object from a Standard Algebraic Notation
        string.

        :param san: Standard Algebraic Notation.
        :param position: Chess position _before_ the move is performed.
        :type position: :class:`Position`
        :param ruleset: Game ruleset.
        :param strict: Only accept the strictest possible notation as valid.
        :return: A move.
        :raise ValueError: *san* is invalid.
        """
        if not strict:
            san = stripped_san(san)
        match = SAN_PATTERN.match(san)
        castling = 'O-O' in san
        if not match:
            if not castling:
                raise ValueError('{!r} is not a valid notation'.format(san))
        else:
            piece, file, rank, destination, promotion = match.groups()

        for move in ruleset.moves(position):
            move_san = move.san(position, ruleset)
            if not strict:
                move_san = stripped_san(move_san)
            if move_san == san:
                return move
            # pylint: disable=too-many-boolean-expressions
            if (
                    strict
                    or castling
                    or move.destination != destination
                    or (file and move.origin.file != file)
                    or (rank and str(move.origin.rank) != rank)
                    or (piece and move.piece.type != Type(piece.lower()))
                    or (promotion
                        and move.promotion != Type(promotion.lower()))
                    or (not piece and move.piece.type != Type.PAWN)):
                continue
            if not promotion and move.promotion:
                break
            return move

        raise ValueError('{!r} is not a valid move'.format(san))

    def _disambiguate_san(
            self,
            position,
            ruleset) -> str:
        """Find the *origin* coordinates (either file or rank or both) that
        might be necessary to disambiguate a SAN move.

        If the rank is enough to disambiguate by, use solely the rank.  If the
        file is enough to disambiguate by, use solely the file.  Else, use
        both.
        """
        file = ''
        rank = ''
        for move in ruleset.moves(position):
            if (move.piece == self.piece
                    and move.destination == self.destination
                    and move != self):
                if move.origin.file == self.origin.file:
                    rank = str(self.origin.rank)
                elif move.origin.rank == self.origin.rank:
                    file = self.origin.file
        return '{}{}'.format(file, rank)


class HistoryRecord(namedtuple('HistoryRecord', ['position', 'move'])):
    """A history record.  This object is immutable.

    You may put these in a list to keep track of a game's history.
    """
    __slots__ = ()

    def __new__(cls, position, move: Move) -> 'HistoryRecord':
        """:param position: Position before *move* is executed.
        :type position: :class:`Position`
        :param move: Move chosen by the player.
        """
        return super().__new__(cls, position, move)


class Gameover(Enum):
    """How a game has ended.  There is no value for 'game has not ended'."""
    CHECKMATE = 1
    STALEMATE = 2
    FIFTY_MOVE = 3
    INSUFFICIENT_MATERIAL = 4
    THREEFOLD_REPETITION = 5
