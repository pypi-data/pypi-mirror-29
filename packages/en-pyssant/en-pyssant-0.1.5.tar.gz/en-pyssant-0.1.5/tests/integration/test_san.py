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

"""Integrated tests for SAN parsing."""

# pylint: disable=invalid-name

import pytest

from en_pyssant import CastlingAvailability, Move, Position, Side, Type, rules


def test_san_simple_pawn_move(position):
    """Return solely the destination of a simple pawn move."""
    san = 'a3'
    move = Move('a2', 'a3')
    move = move.expand(position, rules)
    assert move.san(position, rules) == san
    assert move == Move.from_san(san, position, rules)


def test_san_simple_pawn_move_push(position):
    """Return solely the destination of a simple pawn push."""
    san = 'a4'
    move = Move('a2', 'a4')
    move = move.expand(position, rules)
    assert move.san(position, rules) == san
    assert move == Move.from_san(san, position, rules)


def test_san_simple_knight_move(position):
    """Return the type followed by destination."""
    san = 'Na3'
    move = Move('b1', 'a3')
    move = move.expand(position, rules)
    assert move.san(position, rules) == san
    assert move == Move.from_san(san, position, rules)


def test_san_en_passant_capture(b):
    """Return pawn capture notation."""
    san = 'gxh6'
    position = Position(board=b.EN_PASSANT_BOARD, en_passant_target='h6')
    move = Move('g5', 'h6')
    move = move.expand(position, rules)
    assert move.san(position, rules) == san
    assert move == Move.from_san(san, position, rules)


def test_san_kingside_castling_move(b):
    """Return kingside castling notation."""
    san = 'O-O'
    position = Position(board=b.CASTLING_BOARD)
    move = Move('e1', 'g1')
    move = move.expand(position, rules)
    assert move.san(position, rules) == san
    assert move == Move.from_san(san, position, rules)


def test_san_queenside_castling_move(b):
    """Return queenside castling notation."""
    san = 'O-O-O'
    position = Position(board=b.CASTLING_BOARD)
    move = Move('e1', 'c1')
    move = move.expand(position, rules)
    assert move.san(position, rules) == san
    assert move == Move.from_san(san, position, rules)


def test_san_check(san_position):
    """Return check notation."""
    san = 'Rxc7+'
    move = Move('c2', 'c7')
    move = move.expand(san_position, rules)
    assert move.san(san_position, rules) == san
    assert move == Move.from_san(san, san_position, rules)


def test_san_checkmate(san_position):
    """Return checkmate notation."""
    san = 'Rxa2#'
    move = Move('c2', 'a2')
    move = move.expand(san_position, rules)
    assert move.san(san_position, rules) == san
    assert move == Move.from_san(san, san_position, rules)


def test_san_disambiguous_file_move(san_position):
    """Return file disambiguator notation."""
    san = 'B7xg6'
    move = Move('f7', 'g6')
    move = move.expand(san_position, rules)
    assert move.san(san_position, rules) == san
    assert move == Move.from_san(san, san_position, rules)


def test_san_disambiguous_rank_move(san_position):
    """Return rank disambiguator notation."""
    san = 'Bhxg6'
    move = Move('h5', 'g6')
    move = move.expand(san_position, rules)
    assert move.san(san_position, rules) == san
    assert move == Move.from_san(san, san_position, rules)


def test_san_doubly_disambiguous_move(san_position):
    """Return rank and file disambiguator notation."""
    san = 'Bf5xg6'
    move = Move('f5', 'g6')
    move = move.expand(san_position, rules)
    assert move.san(san_position, rules) == san
    assert move == Move.from_san(san, san_position, rules)


def test_san_castlemate_move(b):
    """Return both castling and checkmate notation."""
    san = 'O-O#'
    position = Position(board=b.CASTLEMATE_BOARD,
                        castling={
                            Side.WHITE: CastlingAvailability(True, True),
                            Side.BLACK: CastlingAvailability(False, False),
                        })
    move = Move('e1', 'g1')
    move = move.expand(position, rules)
    assert move.san(position, rules) == san
    assert move == Move.from_san(san, position, rules)


def test_san_promotion(san_position):
    """Return promotion notation."""
    types = [Type.QUEEN, Type.ROOK, Type.BISHOP, Type.KNIGHT]
    for type_ in types:
        san = 'h8{}'.format(type_.value.upper())
        move = Move('h7', 'h8', promotion=type_)
        move = move.expand(san_position, rules)
        assert move.san(san_position, rules) == san
        assert move == Move.from_san(san, san_position, rules)


def test_san_no_promotion(san_position):
    """If the pawn should promote, but not promotion is specified, raise a
    ValuError.
    """
    san = 'h8'
    with pytest.raises(ValueError):
        Move.from_san(san, san_position, rules)


def test_from_san_false_input(position):
    """An incorrect notation does not a Move make."""
    san = 'Ka3'
    with pytest.raises(ValueError):
        Move.from_san(san, position, rules)


def test_from_san_strict(position):
    """Only accept the strictest notation when strict is given as parameter."""
    san = 'Pa3'
    with pytest.raises(ValueError):
        Move.from_san(san, position, rules, strict=True)
