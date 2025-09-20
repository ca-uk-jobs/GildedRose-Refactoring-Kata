# -*- coding: utf-8 -*-
import unittest

from gilded_rose import GildedRose
from item_factory import make_item


class GildedRoseTest(unittest.TestCase):
    def test_normal_item_before_sell_date(self):
        items = [make_item("foo", 5, 10)]
        GildedRose(items).update_quality()
        self.assertEqual((4, 9), (items[0].sell_in, items[0].quality))

    def test_normal_item_after_sell_date_degrades_twice(self):
        items = [make_item("bar", 0, 10)]
        GildedRose(items).update_quality()
        self.assertEqual((-1, 8), (items[0].sell_in, items[0].quality))

    def test_quality_never_negative(self):
        items = [make_item("foo", 5, 0)]
        GildedRose(items).update_quality()
        self.assertEqual(0, items[0].quality)

    def test_brie_increases_quality_capped_at_50(self):
        items = [make_item("Aged Brie", 2, 49)]
        GildedRose(items).update_quality()
        self.assertEqual((1, 50), (items[0].sell_in, items[0].quality))

    def test_brie_after_sell_date_increases_faster(self):
        items = [make_item("Aged Brie", 0, 48)]
        GildedRose(items).update_quality()
        self.assertEqual((-1, 50), (items[0].sell_in, items[0].quality))

    def test_backstage_thresholds_and_drop_to_zero(self):
        items = [
            make_item("Backstage passes to a TAFKAL80ETC concert", 11, 40),
            make_item("Backstage passes to a TAFKAL80ETC concert", 10, 40),
            make_item("Backstage passes to a TAFKAL80ETC concert", 5, 40),
            make_item("Backstage passes to a TAFKAL80ETC concert", 0, 40),
        ]
        GildedRose(items).update_quality()
        self.assertEqual((10, 41), (items[0].sell_in, items[0].quality))  # +1
        self.assertEqual((9, 42), (items[1].sell_in, items[1].quality))  # +2
        self.assertEqual((4, 43), (items[2].sell_in, items[2].quality))  # +3
        self.assertEqual((-1, 0), (items[3].sell_in, items[3].quality))  # drop to 0

    def test_sulfuras_never_changes(self):
        items = [make_item("Sulfuras, Hand of Ragnaros", 10, 80)]
        GildedRose(items).update_quality()
        self.assertEqual((10, 80), (items[0].sell_in, items[0].quality))

    def test_conjured_degrades_twice_before_sell_date(self):
        items = [make_item("Conjured Mana Cake", 3, 10)]
        GildedRose(items).update_quality()
        self.assertEqual((2, 8), (items[0].sell_in, items[0].quality))

    def test_conjured_degrades_four_after_sell_date(self):
        items = [make_item("Conjured Bread", 0, 10)]
        GildedRose(items).update_quality()
        self.assertEqual((-1, 6), (items[0].sell_in, items[0].quality))

    def test_conjured_quality_never_negative(self):
        items = [make_item("Conjured Mana Cake", 1, 1)]
        GildedRose(items).update_quality()
        self.assertEqual((0, 0), (items[0].sell_in, items[0].quality))


if __name__ == '__main__':
    unittest.main()
