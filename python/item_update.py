# -*- coding: utf-8 -*-

from item_classifier import classify


def _clamp_quality(item):
    """Clamp quality to legal bounds; Sulfuras stays at 80."""
    item_type = classify(item.name)
    if item_type == "sulfuras":
        return
    if item.quality < 0:
        item.quality = 0
    elif item.quality > 50:
        item.quality = 50


def _dec_sell_in(item):
    """Sulfuras is never sold; others decrement."""
    item_type = classify(item.name)
    if item_type != "sulfuras":
        item.sell_in -= 1


def _inc_q(item, n=1):
    """Increment quality by 1"""
    item.quality += n
    _clamp_quality(item)


def _dec_q(item, n=1):
    """Decrement quality by 1"""
    item.quality -= n
    _clamp_quality(item)
