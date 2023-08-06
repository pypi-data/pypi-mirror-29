# -*- coding: utf-8 -*-
#
# Copyright (C) 2018  Carmen Bianca Bakker <carmen@carmenbianca.eu>
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

"""Integrated tests for expanding Move objects."""

# pylint: disable=invalid-name

from en_pyssant import Move, MoveFlag, Piece, Position, Side, Type, rules


def test_expand_simple_advance(position):
    """The *piece* field is correctly added in a simple advance."""
    result = Move('a2', 'a3').expand(position, rules)
    assert result == Move(
        'a2', 'a3', piece=Piece(Type.PAWN, Side.WHITE),
        flags={MoveFlag.NON_CAPTURE})


def test_expand_push_advance(position):
    """The correct flags are added when doing a push advance."""
    result = Move('a2', 'a4').expand(position, rules)
    assert result == Move(
        'a2', 'a4', piece=Piece(Type.PAWN, Side.WHITE),
        flags={MoveFlag.NON_CAPTURE, MoveFlag.PAWN_PUSH})


def test_expand_simple_capture(san_position):
    """Move is correctly expanded for a simple capture."""
    result = Move('c2', 'c7').expand(san_position, rules)
    assert result == Move(
        'c2', 'c7', piece=Piece(Type.ROOK, Side.WHITE),
        captured=Piece(Type.PAWN, Side.BLACK),
        flags={MoveFlag.STANDARD_CAPTURE})


def test_expand_en_passant_capture(b):
    """Move is correctly expanded for an en passant capture."""
    position = Position(board=b.EN_PASSANT_BOARD, en_passant_target='h6')
    result = Move('g5', 'h6').expand(position, rules)
    assert result == Move(
        'g5', 'h6', piece=Piece(Type.PAWN, Side.WHITE),
        captured=Piece(Type.PAWN, Side.BLACK),
        flags={MoveFlag.EN_PASSANT_CAPTURE})


def test_expand_promotion(san_position):
    """The promotion field is correctly filled in."""
    types = [Type.QUEEN, Type.ROOK, Type.BISHOP, Type.KNIGHT]
    for type_ in types:
        result = Move('h7', 'h8', promotion=type_).expand(san_position, rules)
        assert result == Move(
            'h7', 'h8', piece=Piece(Type.PAWN, Side.WHITE),
            promotion=type_,
            flags={MoveFlag.NON_CAPTURE, MoveFlag.PROMOTION})


def test_expand_kingside_castling(b):
    """The castling flag is filled in."""
    position = Position(board=b.CASTLING_BOARD)
    result = Move('e1', 'g1').expand(position, rules)
    assert result == Move(
        'e1', 'g1', piece=Piece(Type.KING, Side.WHITE),
        flags={MoveFlag.NON_CAPTURE, MoveFlag.KINGSIDE_CASTLING})


def test_expand_queenside_castling(b):
    """The castling flag is filled in."""
    position = Position(board=b.CASTLING_BOARD)
    result = Move('e1', 'c1').expand(position, rules)
    assert result == Move(
        'e1', 'c1', piece=Piece(Type.KING, Side.WHITE),
        flags={MoveFlag.NON_CAPTURE, MoveFlag.QUEENSIDE_CASTLING})
