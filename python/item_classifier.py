# -*- coding: utf-8 -*-

import re
from typing import Literal

ItemKind = Literal["sulfuras", "backstage_passes", "aged_brie", "conjured", "normal"]

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


def classify(name: str) -> ItemKind:
    """
    Phrase-based, case-insensitive item classifier.
    Returns one of: 'sulfuras' | 'backstage_passes' | 'aged_brie' | 'conjured' | 'normal'.
    """
    n = normalise(name)

    # 1) Special items first
    if RE_SULFURAS.search(n):
        return "sulfuras"
    if RE_BACKSTAGE_PASSES.search(n):
        return "backstage_passes"
    if RE_AGED_BRIE.search(n):
        return "aged_brie"

    # 2) Conjured item
    if RE_CONJURED.search(n):
        return "conjured"

    # 3) Default
    return "normal"
