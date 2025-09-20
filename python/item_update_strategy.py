# -*- coding: utf-8 -*-

from typing import Protocol
from item_update import _inc_q, _dec_q, _dec_sell_in


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

    def update(self, item):
        _inc_q(item, 1)
        _dec_sell_in(item)
        if item.sell_in < 0:
            _inc_q(item, 1)  # legacy emergent behaviour


class _BackstagePassesStrategy:
    """ Increment quality +1, when sell_in <= 10 increment twice, when sell_in <= 5 increment three times.
        Decrease sell_in. When sell_in < 0 quality is 0
    """

    def update(self, item):
        _inc_q(item, 1)
        if item.sell_in <= 10:
            _inc_q(item, 1)
        if item.sell_in <= 5:
            _inc_q(item, 1)
        _dec_sell_in(item)
        if item.sell_in < 0:
            item.quality = 0


class _NormalStrategy:
    """ Decreases quality -1 when sell_in >=0, decreases quality -2 when sell_in <0. Decrease Sell-In."""

    def update(self, item):
        _dec_q(item, 1)
        _dec_sell_in(item)
        if item.sell_in < 0:
            _dec_q(item, 1)


class _ConjuredNormalStrategy:
    """Conjured behaves like normal, but with a 2× degradation multiplier."""

    def update(self, item):
        # before sell date: -2
        _dec_q(item, 2)
        _dec_sell_in(item)
        if item.sell_in < 0:
            # after sell date: an additional -2 (total -4 per day)
            _dec_q(item, 2)


_STRATEGIES_COLLECTION: dict[str, type[_Strategy]] = {
    "sulfuras": _SulfurasStrategy(),
    "backstage_passes": _BackstagePassesStrategy(),
    "aged_brie": _AgedBrieStrategy(),
    "conjured": _ConjuredNormalStrategy(),
    "normal": _NormalStrategy(),
}


def _pick_strategy(kind: str) -> _Strategy:
    """ Pick appropriate strategy from _STRATEGIES_COLLECTION.
    Default Normal Strategy if item type has no strategy. """

    return _STRATEGIES_COLLECTION.get(kind, _NormalStrategy())
