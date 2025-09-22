# -*- coding: utf-8 -*-

from gilded_rose import Item
from item_classifier import classify
from item_types import ItemType

MIN_QUALITY = 0
MAX_QUALITY = 50
SULFURAS_QUALITY = 80


def _assert_int(name: str, value, field: str) -> None:
    if not isinstance(value, int):
        raise TypeError(f"{field} for '{name}' must be int, got {type(value).__name__}")


def _validate_quality(item_type: ItemType, quality: int) -> int:
    if item_type is ItemType.SULFURAS:
        if quality != SULFURAS_QUALITY:
            raise ValueError("Sulfuras must have quality 80")
        return SULFURAS_QUALITY
    if not (MIN_QUALITY <= quality <= MAX_QUALITY):
        raise ValueError(f"quality must be between {MIN_QUALITY} and {MAX_QUALITY} (got {quality})")
    return quality


def make_item(name: str, sell_in: int, quality: int) -> Item:
    """
    Build a valid Item.
    - Uses `classify(name)` to determine item type.
    - Validates quality values: All non-Sulfuras must start with 0 <= quality <= 50, All Sulfuras must have quality 80.
    - `sell_in` may be negative.
    """
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name must be a non-empty string")

    _assert_int(name, sell_in, "sell_in")
    _assert_int(name, quality, "quality")

    item_type = classify(name)
    quality = _validate_quality(item_type, quality)

    return Item(name, sell_in, quality)
