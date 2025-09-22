# -*- coding: utf-8 -*-

import unittest

from gilded_rose import Item
from item_factory import make_item
from item_classifier import classify
from item_types import ItemType as IT


class TestItemFactory(unittest.TestCase):

    # --- Validate correctness --------------------------------------------------------
    def test_make_item_normal_ok(self):
        item = make_item("foo", 5, 10)
        self.assertIsInstance(item, Item)
        self.assertEqual(("foo", 5, 10), (item.name, item.sell_in, item.quality))

    def test_make_item_allows_negative_sell_in(self):
        item = make_item("foo", -3, 10)
        self.assertEqual(-3, item.sell_in)

    def test_make_item_aged_brie_ok(self):
        item = make_item("Aged Brie", 2, 50)
        self.assertEqual(("Aged Brie", 2, 50), (item.name, item.sell_in, item.quality))

    def test_make_item_aged_brie_regex_ok(self):
        item = make_item("10 yo Aged Brie", 2, 50)
        self.assertEqual(("10 yo Aged Brie", 2, 50), (item.name, item.sell_in, item.quality))

    def test_make_item_backstage_ok(self):
        item = make_item("Backstage passes to a TAFKAL80ETC concert", 15, 20)
        self.assertEqual(("Backstage passes to a TAFKAL80ETC concert", 15, 20), (item.name, item.sell_in, item.quality))

    def test_make_item_backstage_regex_ok(self):
        item = make_item("to a TAFKAL80ETC concert Backstage passes", 15, 20)
        self.assertEqual(("to a TAFKAL80ETC concert Backstage passes", 15, 20), (item.name, item.sell_in, item.quality))

    def test_make_item_sulfuras_quality_80_ok(self):
        item = make_item("Sulfuras, Hand of Ragnaros", 0, 80)
        self.assertEqual(("Sulfuras, Hand of Ragnaros", 0, 80), (item.name, item.sell_in, item.quality))

    def test_make_item_sulfuras_quality_80_regex_ok(self):
        item = make_item("Hand of Ragnaros Sulfuras,", 0, 80)
        self.assertEqual(("Hand of Ragnaros Sulfuras,", 0, 80), (item.name, item.sell_in, item.quality))

    def test_make_item_conjured_ok(self):
        item = make_item("Conjured Mana Cake", 3, 6)
        self.assertEqual(("Conjured Mana Cake", 3, 6), (item.name, item.sell_in, item.quality))

    def test_make_item_conjured_regex_ok(self):
        item = make_item("The Conjured Mana Cake", 3, 6)
        self.assertEqual(("The Conjured Mana Cake", 3, 6), (item.name, item.sell_in, item.quality))

    # --- Validate errors --------------------------------------------------
    def test_make_item_sulfuras_wrong_quality_raises(self):
        with self.assertRaises(ValueError):
            make_item("Sulfuras, Hand of Ragnaros", 0, 79)

    def test_make_item_quality_below_zero_raises(self):
        with self.assertRaises(ValueError):
            make_item("foo", 1, -1)

    def test_make_item_non_sulfuras_quality_above_50_raises(self):
        with self.assertRaises(ValueError):
            make_item("Aged Brie", 5, 51)

    def test_make_item_rejects_non_int_quality(self):
        with self.assertRaises(TypeError):
            make_item("foo", 1, "10")

    def test_make_item_rejects_non_int_sell_in(self):
        with self.assertRaises(TypeError):
            make_item("foo", "5", 10)

    def test_make_item_rejects_empty_name(self):
        with self.assertRaises(ValueError):
            make_item("   ", 1, 10)

    # --- Validate classifier
    def test_backstage_passes_phrase_only(self):
        assert classify("Backstage passes") is IT.BACKSTAGE_PASSES
        assert classify("BACKSTAGE   PASSES, VIP") is IT.BACKSTAGE_PASSES
        assert classify("backstage pass") is IT.NORMAL
        assert classify("backstage VIP passes") is IT.NORMAL

    def test_aged_brie_phrase_only(self):
        assert classify("AGED BRIE") is IT.AGED_BRIE
        assert classify("brie aged") is IT.NORMAL  # phrase must be together

    def test_sulfuras_anywhere(self):
        assert classify("sulfuras, hand of ragnaros") is IT.SULFURAS
        assert classify("something else sulfuras") is IT.SULFURAS

    def test_conjured_token_anywhere(self):
        assert classify("very CONJURED mana cake") is IT.CONJURED


if __name__ == "__main__":
    unittest.main()
