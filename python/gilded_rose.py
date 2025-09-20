# -*- coding: utf-8 -*-

from item_classifier import classify
from item_update import _dec_q, _dec_sell_in, _inc_q


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            item_type = classify(item.name)
            if item_type == "sulfuras":
                continue
            if item_type == "backstage_passes":
                _inc_q(item, 1)
                if item.sell_in <= 10:
                    _inc_q(item, 1)
                if item.sell_in <= 5:
                    _inc_q(item, 1)
                _dec_sell_in(item)
                if item.sell_in < 0:
                    item.quality = 0
                continue
            if item_type == "aged_brie":
                _inc_q(item, 1)
                _dec_sell_in(item)
                if item.sell_in < 0:
                    _inc_q(item, 1)
                continue
            if item_type == "conjured":
                _dec_q(item, 2)
                _dec_sell_in(item)
                if item.sell_in < 0:
                    _dec_q(item, 2)
                continue
            if item_type == "normal":
                _dec_q(item, 1)
                _dec_sell_in(item)
                if item.sell_in < 0:
                    _dec_q(item, 1)
                continue


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
