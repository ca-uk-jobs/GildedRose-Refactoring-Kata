# -*- coding: utf-8 -*-

from item_types import ItemType


def _clamp_quality(item, item_type: ItemType):
    """Clamp quality to legal bounds; Sulfuras stays at 80."""
    if item_type is ItemType.SULFURAS:
        return
    if item.quality < 0:
        item.quality = 0
    elif item.quality > 50:
        item.quality = 50


def _dec_sell_in(item, item_type: ItemType):
    """Sulfuras is never sold; others decrement."""
    if item_type is not ItemType.SULFURAS:
        item.sell_in -= 1


def _inc_q(item, item_type: ItemType, n=1):
    """Increment quality by 1"""
    item.quality += n
    _clamp_quality(item, item_type)


def _dec_q(item, item_type: ItemType, n=1):
    """Decrement quality by 1"""
    item.quality -= n
    _clamp_quality(item, item_type)
