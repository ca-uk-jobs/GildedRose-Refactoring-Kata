# -*- coding: utf-8 -*-

import re
from item_types import ItemType

# Very simple normaliser: collapse whitespace and lowercase
_ws = re.compile(r"\s+")


def normalise(name: str) -> str:
    return _ws.sub(" ", name).strip().lower()


# Exact phrase patterns
_phrase = lambda w: re.compile(rf"\b{w}\b")

RE_SULFURAS = _phrase("sulfuras")
RE_BACKSTAGE_PASSES = _phrase("backstage passes")
RE_AGED_BRIE = _phrase("aged brie")
RE_CONJURED = _phrase("conjured")

# Precedence matters (specials first)
_PATTERNS: list[tuple[re.Pattern, ItemType]] = [
    (RE_SULFURAS, ItemType.SULFURAS),
    (RE_BACKSTAGE_PASSES, ItemType.BACKSTAGE_PASSES),
    (RE_AGED_BRIE, ItemType.AGED_BRIE),
    (RE_CONJURED, ItemType.CONJURED),
]


def classify(name: str) -> ItemType:
    """
    Phrase-based, case-insensitive item classifier.
    Returns one ItemType.
    """
    n = normalise(name)

    for rex, kind in _PATTERNS:
        if rex.search(n):
            return kind
    return ItemType.NORMAL
