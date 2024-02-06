# pylint: disable=missing-docstring

import unittest

from src.tiled_tools.common.grid import Grid, HexGrid, WrapDirection
from src.tiled_tools.map.algorithms import QuantumState, WaveFunctionCollapse
from src.tiled_tools.map.map import ISLAND_RULESET, TileType


class TestQuantumState(unittest.TestCase):
    def setUp(self) -> None:
        self.state = QuantumState(TileType)

    def test_init(self):
        self.assertListEqual(
            self.state.possible_states,
            [
                TileType.OCEAN,
                TileType.SAND,
                TileType.FOREST,
                TileType.STONE,
                TileType.GRASS,
            ],
        )

    def test_collapse(self):
        self.state.collapse(TileType.OCEAN)
        self.assertListEqual(self.state.possible_states, [TileType.OCEAN])

        self.state.collapse(TileType.SAND)
        self.assertListEqual(self.state.possible_states, [TileType.SAND])

    def test_remove_contrary_state(self):
        self.state.remove_contrary_states(TileType.OCEAN, ISLAND_RULESET)
        self.assertListEqual(
            self.state.possible_states, [TileType.OCEAN, TileType.SAND]
        )

        self.state.collapse(TileType.OCEAN)
        self.state.remove_contrary_states(TileType.OCEAN, ISLAND_RULESET)
        self.assertListEqual(self.state.possible_states, [TileType.OCEAN])

    def test_remove_contrary_state_stone(self):
        self.state.remove_contrary_states(TileType.STONE, ISLAND_RULESET)
        self.assertListEqual(
            self.state.possible_states,
            [TileType.SAND, TileType.FOREST, TileType.STONE, TileType.GRASS],
        )

        self.state.collapse(TileType.STONE)
        self.state.remove_contrary_states(TileType.STONE, ISLAND_RULESET)
        self.assertListEqual(self.state.possible_states, [TileType.STONE])


class TestWaveFunctionCollapse(unittest.TestCase):
    def setUp(self) -> None:
        simple_island_values = [
            [QuantumState(TileType) for _c in range(10)] for _r in range(10)
        ]
        simple_grid = Grid(simple_island_values, wrap_direction=WrapDirection.NONE)
        desired_ratios = {TileType.STONE: 0.5, TileType.OCEAN: 0.5}
        advanced_grid = HexGrid(simple_island_values, wrap_direction=WrapDirection.TORUS)

        self.wfc = WaveFunctionCollapse(ISLAND_RULESET, simple_grid, desired_ratios)
        self.adv_wfc = WaveFunctionCollapse(ISLAND_RULESET, advanced_grid, desired_ratios)

    def test_collapse(self):
        self.wfc.collapse()
        self.assertTrue(len(self.wfc.uncollapsed()) == 0)

        self.adv_wfc.collapse()
        self.assertTrue(len(self.adv_wfc.uncollapsed()) == 0)


