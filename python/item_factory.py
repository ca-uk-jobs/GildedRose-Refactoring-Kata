# -*- coding: utf-8 -*-

from gilded_rose import Item
from item_classifier import classify


def _assert_int(name: str, value, field: str) -> None:
    if not isinstance(value, int):
        raise TypeError(f"{field} for '{name}' must be int, got {type(value).__name__}")


def _validate_quality_range(quality: int) -> bool:
    if not (0 <= quality <= 50):
        return False
    return True


def _canonicalise_quality(kind: str, quality: int) -> int:
    if kind == "sulfuras":
        if quality != 80:
            raise ValueError("Sulfuras must have quality 80")
        return quality
    if _validate_quality_range(quality):
        return quality
    raise ValueError(f"quality must be between 0 and 50 inclusive (got {quality})")


def make_item(name: str, sell_in: int, quality: int) -> Item:
    """
    Build a valid Item.
    - Uses `classify(name)` to determine if this is Sulfuras (validates quality=80).
    - All non-Sulfuras must start with 0 <= quality <= 50.
    - `sell_in` may be negative.
    """
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name must be a non-empty string")

    _assert_int(name, sell_in, "sell_in")
    _assert_int(name, quality, "quality")

    item_type = classify(name)
    quality = _canonicalise_quality(item_type, quality)

    return Item(name, sell_in, quality)
