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

"""Unit tests for Position."""

# pylint: disable=invalid-name

from unittest import mock

import pytest

from en_pyssant import CastlingAvailability, Position, Side
from en_pyssant._util import ALL_SQUARES


def _create_fen_string(**kwargs):
    board = kwargs.get(
        'board',
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
    side_to_play = kwargs.get('side_to_play', 'w')
    castling = kwargs.get('castling', 'KQkq')
    en_passant_target = kwargs.get('en_passant_target', '-')
    half_move_clock = kwargs.get('half_move_clock', '0')
    move_count = kwargs.get('move_count', '1')

    return ' '.join(
        [board, side_to_play, castling, en_passant_target, half_move_clock,
         move_count])


def test_repr_board(position):
    """The board portion of Position.__repr__ is equal to Board.__repr__."""
    assert repr(position).split()[0] == repr(position.board)


def test_repr_side_to_play(position):
    """The side-to-play portion of Position.__repr__ is either 'w' or 'b'."""
    assert repr(position).split()[1] == 'w'
    assert repr(Position(side_to_play=Side.BLACK)).split()[1] == 'b'


def test_repr_castling(position):
    """The castling portion of Position.__repr__ is correct."""
    assert repr(position).split()[2] == 'KQkq'
    no_castling = ({
        Side.WHITE: CastlingAvailability(False, False),
        Side.BLACK: CastlingAvailability(False, False)
    }, '-')
    no_kingside = ({
        Side.WHITE: CastlingAvailability(False, True),
        Side.BLACK: CastlingAvailability(False, True)
    }, 'Qq')
    no_queenside = ({
        Side.WHITE: CastlingAvailability(True, False),
        Side.BLACK: CastlingAvailability(True, False)
    }, 'Kk')
    for thing in [no_castling, no_kingside, no_queenside]:
        assert repr(Position(castling=thing[0])).split()[2] == thing[1]


def test_repr_en_passant_target(position):
    """The en-passant-target portion of Position.__repr__ is either a
    a square or '-'.
    """
    assert repr(position).split()[3] == '-'
    for square in ALL_SQUARES:
        new_position = Position(en_passant_target=square)
        assert repr(new_position).split()[3] == square


def test_repr_half_move_clock(position):
    """The half-move-clock portion of Position.__repr__ is correct."""
    assert repr(position).split()[4] == '0'
    for i in range(51):
        new_position = Position(half_move_clock=i)
        assert repr(new_position).split()[4] == str(i)


def test_repr_move_count(position):
    """The move-count portion of Position.__repr__ is correct."""
    assert repr(position).split()[5] == '1'
    for i in range(1, 100):
        new_position = Position(move_count=i)
        assert repr(new_position).split()[5] == str(i)


def test_from_fen(position, BoardMock):
    """Position.from_fen correctly creates an initial position from a
    FEN string.
    """
    fen = _create_fen_string()
    initial_position = Position.from_fen(fen, board_cls=BoardMock)
    assert position == initial_position
    BoardMock.from_fen.assert_called_once_with(fen.split()[0])


def test_from_fen_wrong_length(BoardMock):
    """Position.from_fen raises a ValueError when the provided string
    does not have the correct amount of sections.
    """
    correct_fen = _create_fen_string()
    too_long = correct_fen + ' 1'
    with pytest.raises(ValueError):
        Position.from_fen(too_long, board_cls=BoardMock)
    too_short = ''.join(correct_fen.split()[:6])
    with pytest.raises(ValueError):
        Position.from_fen(too_short, board_cls=BoardMock)


def test_from_fen_incorrect_board(BoardMock):
    """Position.from_fen raises a ValueError when provided an incorrect
    board.
    """
    BoardMock.from_fen.side_effect = ValueError()

    with pytest.raises(ValueError):
        Position.from_fen(_create_fen_string(), board_cls=BoardMock)


def test_from_fen_incorrect_side_to_play(BoardMock):
    """Position.from_fen raises a ValueError when provided an incorrect
    side-to-play.
    """
    incorrect_sides_to_play = [
        'W',
        'B',
        'white',
        'black',
        'hello'
    ]
    for side_to_play in incorrect_sides_to_play:
        with pytest.raises(ValueError):
            Position.from_fen(
                _create_fen_string(
                    side_to_play=side_to_play,
                    board_cls=BoardMock))


def test_from_fen_side_to_play(BoardMock):
    """Correctly associate 'w' with white and 'b' with black in
    Position.from_fen.
    """
    sides = {'w': Side.WHITE, 'b': Side.BLACK}
    for key, value in sides.items():
        position = Position.from_fen(
            _create_fen_string(side_to_play=key),
            board_cls=BoardMock)
        assert position.side_to_play == value


def test_from_fen_incorrect_castling(BoardMock):
    """Position.from_fen raises a ValueError when provided an incorrect
    castling.
    """
    incorrect_castlings = [
        'kqKQ',
        'hello',
        'kk',
        'KQkq.'
    ]
    for castling in incorrect_castlings:
        with pytest.raises(ValueError):
            Position.from_fen(
                _create_fen_string(castling=castling), board_cls=BoardMock)


def test_from_fen_incorrect_en_passant_target(BoardMock):
    """Position.from_fen raises a ValueError when provided an incorrect
    en-passant-target.
    """
    incorrect_targets = [
        'hello',
        'a9',
        'a0',
        '1a',
        'i1'
    ]
    for target in incorrect_targets:
        with pytest.raises(ValueError):
            Position.from_fen(
                _create_fen_string(en_passant_target=target),
                board_cls=BoardMock)


def test_from_fen_en_passant_target(BoardMock):
    """When given an en passant target, Position.from_fen correctly parses
    it.
    """
    targets = {
        '-': None,
    }
    for square in ALL_SQUARES:
        targets[square] = square

    for key, value in targets.items():
        position = Position.from_fen(
            _create_fen_string(en_passant_target=key),
            board_cls=BoardMock)
        assert position.en_passant_target == value


def test_from_fen_incorrect_half_move_clock(BoardMock):
    """Position.from_fen raises a ValueError when provided an incorrect
    half-move-clock.
    """
    incorrect_clocks = [
        'hello',
        '-1',
        '1.1'
    ]
    for clock in incorrect_clocks:
        with pytest.raises(ValueError):
            Position.from_fen(
                _create_fen_string(half_move_clock=clock),
                board_cls=BoardMock)


def test_from_fen_half_move_clock(BoardMock):
    """When given a half move clock, Position.from_fen correctly parses it.
    """
    clocks = [i for i in range(51)]
    for clock in clocks:
        position = Position.from_fen(
            _create_fen_string(half_move_clock=str(clock)),
            board_cls=BoardMock)
        assert position.half_move_clock == clock


def test_from_fen_incorrect_move_count(BoardMock):
    """Position.from_fen raises a ValueError when provided an incorrect
    move count.
    """
    incorrect_counts = [
        'hello',
        '-1',
        '0',
        '1.1'
    ]
    for count in incorrect_counts:
        with pytest.raises(ValueError):
            Position.from_fen(
                _create_fen_string(move_count=count),
                board_cls=BoardMock)


def test_from_fen_move_count(BoardMock):
    """When given a move count, Position.from_fen correctly parses it."""
    counts = [i for i in range(1, 100)]
    for count in counts:
        position = Position.from_fen(
            _create_fen_string(move_count=str(count)),
            board_cls=BoardMock)
        assert position.move_count == count


def test_repr_from_fen(position, BoardMock):
    """The output of Position.__repr__ can be forwarded to
    Position.from_fen to create an identical object.
    """
    assert Position.from_fen(repr(position), board_cls=BoardMock) == position


def test_pretty():
    """Output a correct position."""
    mock_board = mock.Mock()
    mock_board.pretty.return_value = 'board'
    position = Position(board=mock_board)
    assert position.pretty() == (
        'board\n'
        '\n'
        'FEN: {}'.format(position))
