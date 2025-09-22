# -*- coding: utf-8 -*-

from typing import Protocol, Final
from item_update import _inc_q, _dec_q, _dec_sell_in
from item_types import ItemType


class _Strategy(Protocol):
    def update(self, item) -> None: ...


class _SulfurasStrategy:
    """ Do nothing """

    def update(self, item):
        return None


class _AgedBrieStrategy:
    """ Increment quality +1 when sell_in>=0, increment quality twice when sell_in<0. Decrease Sell-In.
        Quality's 2X increment not explicitly specified, but part of legacy behaviour
    """

    def __init__(self):
        self.item_type = ItemType.AGED_BRIE

    def update(self, item):
        _inc_q(item, self.item_type, 1)
        _dec_sell_in(item, self.item_type)
        if item.sell_in < 0:
            _inc_q(item, self.item_type, 1)  # legacy emergent behaviour


class _BackstagePassesStrategy:
    """ Increment quality +1, when sell_in <= 10 increment twice, when sell_in <= 5 increment three times.
        Decrease sell_in. When sell_in < 0 quality is 0
    """

    def __init__(self):
        self.item_type = ItemType.BACKSTAGE_PASSES

    def update(self, item):
        _inc_q(item, self.item_type, 1)
        if item.sell_in <= 10:
            _inc_q(item, self.item_type, 1)
        if item.sell_in <= 5:
            _inc_q(item, self.item_type, 1)
        _dec_sell_in(item, self.item_type)
        if item.sell_in < 0:
            item.quality = 0


class _NormalStrategy:
    """ Decreases quality -1 when sell_in >=0, decreases quality -2 when sell_in <0. Decrease Sell-In."""

    def __init__(self):
        self.item_type = ItemType.NORMAL

    def update(self, item):
        _dec_q(item, self.item_type, 1)
        _dec_sell_in(item, self.item_type)
        if item.sell_in < 0:
            _dec_q(item, self.item_type, 1)


class _ConjuredNormalStrategy:
    """Conjured behaves like normal, but with a 2× degradation multiplier."""

    def __init__(self):
        self.item_type = ItemType.CONJURED

    def update(self, item):
        # before sell date: -2
        _dec_q(item, self.item_type, 2)
        _dec_sell_in(item, self.item_type)
        if item.sell_in < 0:
            # after sell date: an additional -2 (total -4 per day)
            _dec_q(item, self.item_type, 2)


# Singletons
SULFURAS: Final[_Strategy] = _SulfurasStrategy()
BACKSTAGE_PASSES: Final[_Strategy] = _BackstagePassesStrategy()
AGED_BRIE: Final[_Strategy] = _AgedBrieStrategy()
CONJURED: Final[_Strategy] = _ConjuredNormalStrategy()
NORMAL: Final[_Strategy] = _NormalStrategy()

_STRATEGIES_COLLECTION: dict[ItemType, _Strategy] = {
    ItemType.SULFURAS: SULFURAS,
    ItemType.AGED_BRIE: AGED_BRIE,
    ItemType.BACKSTAGE_PASSES: BACKSTAGE_PASSES,
    ItemType.CONJURED: CONJURED,
    ItemType.NORMAL: NORMAL,
}


def _pick_strategy(item_type: ItemType) -> _Strategy:
    """ Pick appropriate strategy from _STRATEGIES_COLLECTION.
    Default Normal Strategy if item type has no strategy. """

    return _STRATEGIES_COLLECTION.get(item_type, NORMAL)
