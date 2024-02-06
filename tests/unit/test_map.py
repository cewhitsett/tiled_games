# pylint: disable=missing-docstring,line-too-long

import unittest

from src.tiled_tools.map.map import (
    ISLAND_RULESET,
    Tile,
    TileRule,
    TileRuleSet,
    TileType,
)


class TestTileRuleSet(unittest.TestCase):
    def setUp(self) -> None:
        self.tile_rule_set = ISLAND_RULESET

    def test_get_rule(self):
        rule = self.tile_rule_set.get_rule(TileType.OCEAN)

        self.assertIsInstance(rule, TileRule)
        self.assertEqual(rule.tile_type, TileType.OCEAN)

    def test_get_weight(self):
        self.assertEqual(
            self.tile_rule_set.get_weight(TileType.OCEAN, TileType.OCEAN), 0.5
        )
        self.assertEqual(
            self.tile_rule_set.get_weight(TileType.OCEAN, TileType.SAND), 0.5
        )
        self.assertEqual(
            self.tile_rule_set.get_weight(TileType.FOREST, TileType.OCEAN), 0.0
        )
        self.assertEqual(
            self.tile_rule_set.get_weight(TileType.FOREST, TileType.SAND), 0.25
        )

    def test_is_allowed_neighbor(self):
        self.assertTrue(
            self.tile_rule_set.is_allowed_neighbor(TileType.OCEAN, TileType.OCEAN)
        )
        self.assertTrue(
            self.tile_rule_set.is_allowed_neighbor(TileType.OCEAN, TileType.SAND)
        )
        self.assertFalse(
            self.tile_rule_set.is_allowed_neighbor(TileType.FOREST, TileType.OCEAN)
        )
        self.assertFalse(
            self.tile_rule_set.is_allowed_neighbor(TileType.OCEAN, TileType.FOREST)
        )
        self.assertTrue(
            self.tile_rule_set.is_allowed_neighbor(TileType.FOREST, TileType.SAND)
        )
