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

"""A board representation and implementation."""

from abc import ABCMeta, abstractmethod
from functools import lru_cache
from io import StringIO
from typing import Any, Iterator, Optional, Tuple, Union, List

from ._core import Piece, Side, Square, Type  # pylint: disable=unused-import
from ._util import ALL_SQUARES, validate_fen_board


class Board(metaclass=ABCMeta):
    """An abstract base class for a chess board implementation.  A chess board
    is immutable and need implement only :meth:`get`, :meth:`put` and
    :meth:`__init__`.  :meth:`__init__` must take no positional arguments and -
    without any arguments - create an initial chess board.

    All other methods are already implemented.
    """

    @classmethod
    def from_fen(cls, fen: str) -> 'Board':
        """Generate a :class:`Board` from the board portion of a
        Forsyth-Edwards Notation string.

        :param fen: First part of Forsyth-Edwards Notation
        :return: A board.
        :raise ValueError: Input is invalid.
        """
        board = cls()
        fen = fen.split()[0]
        chunks = fen.split('/')
        files = 'abcdefgh'

        if not validate_fen_board(fen):
            raise ValueError('{} is not a valid notation'.format(fen))

        # From white to black
        for rank, chunk in zip(range(1, 9), reversed(chunks)):
            file_position = 0
            for char in chunk:
                if char.isnumeric():
                    for _ in range(int(char)):
                        board = board.put('{}{}'.format(files[file_position],
                                                        rank),
                                          None)
                        file_position += 1
                else:
                    piece = Piece(Type(char.lower()),
                                  Side.WHITE if char.isupper() else Side.BLACK)
                    board = board.put('{}{}'.format(files[file_position],
                                                    rank),
                                      piece)
                    file_position += 1

        return board

    @abstractmethod
    def get(self, square: str) -> Optional[Piece]:
        """Return piece at *square*.  Return :const:`None` if no piece exists
        at square.

        :param square: Square in algebraic notation.
        :return: Piece at square.
        """

    @abstractmethod
    def put(self, square: str, piece: Optional[Piece]) -> 'Board':
        """Put *piece* on *square*.  Override any existing pieces.  Return a
        new board.

        :param square: Square in algebraic notation.
        :param piece: Piece to be placed on square.
        :return: A new board.
        """

    def pretty(self) -> str:
        """
        >>> print(DictBoard().pretty())
          A B C D E F G H
        8 r n b q k b n r
        7 p p p p p p p p
        6 . . . . . . . .
        5 . . . . . . . .
        4 . . . . . . . .
        3 . . . . . . . .
        2 P P P P P P P P
        1 R N B Q K B N R

        :return: A pretty representation of the board.
        """
        result = StringIO()
        result.write('  A B C D E F G H\n')
        for rank in zip(*[iter(ALL_SQUARES)] * 8):
            row = [rank[0][1]]
            for square in rank:
                piece = self[square]
                if not piece:
                    piece = '.'
                else:
                    piece = str(piece)
                row.append(piece)
            result.write(' '.join(row))
            result.write('\n')
        return result.getvalue().rstrip()

    def all_pieces(self) -> Iterator[Tuple[Square, Optional[Piece]]]:
        """Yield all squares and their respective pieces, from a1 to h8.
        Increment files before ranks.

        Comparable to :func:`enumerate`, except for squares and pieces.

        :return: All squares and their respective pieces.
        """
        for square in ALL_SQUARES:
            yield square, self[square]

    def __getitem__(self, key: str) -> Optional[Piece]:
        return self.get(key)

    def __eq__(self, other: Any) -> bool:
        for square in ALL_SQUARES:
            try:
                if self[square] != other[square]:
                    return False
            except:  # pylint: disable=bare-except
                return False
        return True

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        # First divide up in chunks of 8.
        chunks = [[self['{}{}'.format(file_, rank)] for file_ in 'abcdefgh']
                  for rank in reversed(range(1, 9))]
        new_chunks = []

        for chunk in chunks:
            new_chunk = []
            counter = 0
            # Just add each piece to *new_chunk*, unless it's an empty square.
            # Increment *counter* if the square is empty.  Add the value of
            # counter to *new_chunk* when the loop hits a piece, or if it hits
            # the end.
            for piece in chunk:
                if piece:
                    if counter:
                        new_chunk.append(str(counter))
                        counter = 0
                    new_chunk.append(piece.type.value.upper()
                                     if piece.side == Side.WHITE
                                     else piece.type.value)
                else:
                    counter += 1
            if counter:
                new_chunk.append(str(counter))

            # Join the chunks into a single string and append them to
            # *new_chunks*.
            new_chunks.append(''.join(new_chunk))

        # Join the chunks with '/'.
        return '/'.join(new_chunks)


def all_board_classes() -> List[Board]:
    """Return a list of all defined board classes, excluding the base class."""
    result = []
    for key, value in globals().items():
        if key.endswith('Board') and key != 'Board':
            result.append(value)
    return result


@lru_cache(maxsize=64)
def algebraic_to_index(square: Union[Square, str]) -> int:
    """Convert the square in algebraic notation to the corresponding index
    in our internal representation.

    :param square: Algebraic notation square.
    :return: Index on board.
    :raise ValueError: Input is invalid.

    >>> algebraic_to_index('a8')
    0
    >>> algebraic_to_index('h1')
    63
    >>> algebraic_to_index('9a')
    Traceback (most recent call last):
        ...
    ValueError: '9a' is not a valid square
    """
    if not isinstance(square, Square):
        square = Square(square)

    rank = square.rank
    file_ = ord(square.file) - 97

    return (8 - rank) * 8 + (file_)


ALGEBRAIC_TO_INDEX_MAP = dict()
for _square in ALL_SQUARES:
    ALGEBRAIC_TO_INDEX_MAP[_square] = algebraic_to_index(_square)

# Note that white is on TOP.  This is to match a1 with index 0.
_INITIAL_STRINGBOARD = (
    'rnbqkbnr'  # 0-7,   a8-h8
    'pppppppp'  # 8-15,  a7-h7
    '        '  # 16-23, a6-h6
    '        '  # 24-31, a5-h5
    '        '  # 32-39, a4-h4
    '        '  # 40-47, a3-h3
    'PPPPPPPP'  # 48-55, a2-h2
    'RNBQKBNR'  # 56-63, a1-h1
)

_INITIAL_BYTESBOARD = _INITIAL_STRINGBOARD.encode('ascii')

_INITIAL_DICTBOARD = dict()
_INITIAL_LISTBOARD = list()
for _char, _square in zip(_INITIAL_STRINGBOARD, ALL_SQUARES):
    if _char == ' ':
        _piece = None
    else:
        _piece = Piece(Type(_char.lower()), Side.WHITE if _char.isupper() else
                       Side.BLACK)
    _INITIAL_DICTBOARD[_square] = _piece
    _INITIAL_LISTBOARD.append(_piece)


class BytesBoard(Board):
    """A simple bytes-based board representation."""
    # pylint: disable=method-hidden

    def __init__(self, **kwargs):
        self._board = kwargs.get('_board', _INITIAL_BYTESBOARD)
        self.get = lru_cache(maxsize=64)(self.get)

    def get(self, square: str) -> Optional[Piece]:
        i = self._board[ALGEBRAIC_TO_INDEX_MAP[square]]
        letter = bytes((i,))
        if letter == b' ':
            return None
        rtype = Type(letter.lower().decode('ascii'))
        rside = Side.WHITE if letter.isupper() else Side.BLACK
        return Piece(rtype, rside)

    def put(self, square: str, piece: Optional[Piece]) -> 'BytesBoard':
        if piece is None:
            letter = b' '
        else:
            letter = str(piece).encode('ascii')
        index = ALGEBRAIC_TO_INDEX_MAP[square]
        return self.__class__(_board=b''.join([
            self._board[:index],
            letter,
            self._board[index + 1:]
        ]))

    def __hash__(self):
        return hash(self._board) + 1


class DictBoard(Board):
    """A simple dictionary-based board representation."""

    def __init__(self, **kwargs):
        self._board = kwargs.get('_board', _INITIAL_DICTBOARD)

    def get(self, square: str) -> Optional[Piece]:
        return self._board[square]

    def put(self, square: str, piece: Optional[Piece]) -> 'DictBoard':
        # Shallow copy.  This is acceptable, because all values in it are
        # immutable.
        new_dict = self._board.copy()
        new_dict[Square(square)] = piece
        return self.__class__(_board=new_dict)

    def __hash__(self):
        return id(self)


class ListBoard(Board):
    """A simple list-based board representation."""

    def __init__(self, **kwargs):
        self._board = kwargs.get('_board', _INITIAL_LISTBOARD)

    def get(self, square: str) -> Optional[Piece]:
        return self._board[ALGEBRAIC_TO_INDEX_MAP[square]]

    def put(self, square: str, piece: Optional[Piece]) -> 'DictBoard':
        # Shallow copy.  This is acceptable, because all values in it are
        # immutable.
        new_list = self._board[:]
        new_list[ALGEBRAIC_TO_INDEX_MAP[square]] = piece
        return self.__class__(_board=new_list)

    def __hash__(self):
        return id(self)


class StringBoard(Board):
    """A simple string-based board representation."""
    # pylint: disable=method-hidden

    def __init__(self, **kwargs):
        self._board = kwargs.get('_board', _INITIAL_STRINGBOARD)
        self.get = lru_cache(maxsize=64)(self.get)

    def get(self, square: str) -> Optional[Piece]:
        letter = self._board[ALGEBRAIC_TO_INDEX_MAP[square]]
        if letter == ' ':
            return None
        rtype = Type(letter.lower())
        rside = Side.WHITE if letter.isupper() else Side.BLACK
        return Piece(rtype, rside)

    def put(self, square: str, piece: Optional[Piece]) -> 'StringBoard':
        if piece is None:
            letter = ' '
        else:
            letter = str(piece)
        index = ALGEBRAIC_TO_INDEX_MAP[square]
        return self.__class__(_board='{}{}{}'.format(
            self._board[:index],
            letter,
            self._board[index + 1:]
        ))

    def __hash__(self):
        return id(self)
