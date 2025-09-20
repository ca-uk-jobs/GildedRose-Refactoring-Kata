# -*- coding: utf-8 -*-

from item_classifier import classify
from item_update_strategy import _pick_strategy


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            item_type = classify(item.name)
            item_strategy = _pick_strategy(item_type)
            item_strategy.update(item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
