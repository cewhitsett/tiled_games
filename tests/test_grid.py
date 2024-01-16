import numpy as np
import unittest
import snapshottest

from tiled_tools.common.grid import (
    Grid,
    GridGenerator,
    GridType,
    HexGrid,
    WrapDirection,
)


class TestGrid(snapshottest.TestCase):
    def setUp(self):
        self.initial_list = [[None for _ in range(3)] for _ in range(4)]
        self.g = Grid(self.initial_list, wrap_direction=WrapDirection.NONE)

    def test_init(self):
        self.assertEqual(self.g.width, 3)
        self.assertEqual(self.g.height, 4)
        self.assertListEqual(self.g.grid.tolist(), self.initial_list)
        self.assertEqual(self.g.wrap_direction, WrapDirection.NONE)

    def test_get(self):
        self.g.set(0, 0, 1)
        self.g.set(1, 1, 2)
        self.g.set(2, 2, 3)
        self.g.set(2, 3, 4)

        self.assertEqual(self.g.get(0, 0), 1)
        self.assertEqual(self.g.get(1, 1), 2)
        self.assertEqual(self.g.get(2, 2), 3)
        self.assertEqual(self.g.get(2, 3), 4)

    def test_set(self):
        self.g.set(0, 0, 1)
        self.g.set(1, 1, 2)
        self.g.set(2, 2, 99)
        self.g.set(2, 3, 4)

        self.assertEqual(self.g.get(0, 0), 1)
        self.assertEqual(self.g.get(1, 1), 2)
        self.assertEqual(self.g.get(2, 2), 99)
        self.assertEqual(self.g.get(2, 3), 4)

    def test_getitem(self):
        self.g.set(0, 0, 1)
        self.g.set(1, 1, 2)
        self.g.set(2, 2, 3)
        self.g.set(2, 3, 4)

        self.assertEqual(self.g[0, 0], 1)
        self.assertEqual(self.g[1, 1], 2)
        self.assertEqual(self.g[2, 2], 3)
        self.assertEqual(self.g[2, 3], 4)

    def test_setitem(self):
        self.g[0, 0] = 1
        self.g[1, 1] = 2
        self.g[2, 2] = 3
        self.g[2, 3] = 4

        self.assertEqual(self.g[0, 0], 1)
        self.assertEqual(self.g[1, 1], 2)
        self.assertEqual(self.g[2, 2], 3)
        self.assertEqual(self.g[2, 3], 4)

    def test_get_adjacent_cords(self):
        identity = GridGenerator.identity(3)

        self.assertListEqual(identity.get_adjacent_coords(0, 0), [(1, 0), (0, 1)])

        self.assertListEqual(
            identity.get_adjacent_coords(1, 1), [(0, 1), (2, 1), (1, 0), (1, 2)]
        )

        self.assertListEqual(identity.get_adjacent_coords(2, 2), [(1, 2), (2, 1)])

    def test_get_adjacent(self):
        identity = GridGenerator.identity(3)

        self.assertListEqual(identity.get_adjacent(0, 0), [0, 0])

        self.assertListEqual(identity.get_adjacent(1, 1), [0, 0, 0, 0])

        self.assertListEqual(identity.get_adjacent(2, 2), [0, 0])

        self.assertListEqual(identity.get_adjacent(1, 0), [1, 0, 1])


class TestHexGrid(snapshottest.TestCase):
    def setUp(self):
        self.initial_list = [[0 for _i in range(5)] for _j in range(7)]

        self.g = HexGrid(self.initial_list)

    def test_get_adjacent_coords(self):
        self.assertListEqual(self.g.get_adjacent_coords(0, 0), [(0, 1), (1, 0)])

        self.assertListEqual(
            self.g.get_adjacent_coords(1, 1),
            [(1, 0), (1, 2), (0, 1), (0, 2), (2, 1), (2, 2)],
        )

        self.assertListEqual(
            self.g.get_adjacent_coords(2, 2),
            [(2, 1), (2, 3), (1, 1), (1, 2), (3, 1), (3, 2)],
        )

        self.assertListEqual(self.g.get_adjacent_coords(4, 6), [(4, 5), (3, 5), (3, 6)])


class TestGridGenerator(snapshottest.TestCase):
    def setUp(self):
        pass

    def test_identity(self):
        identity = GridGenerator.identity(3)
        self.assertEqual(type(identity), Grid)
        self.assertMatchSnapshot(identity.tolist(), "grid_identity_3")

        identity = GridGenerator.identity(5, GridType.HEX)
        self.assertEqual(type(identity), Grid)
        self.assertMatchSnapshot(identity.tolist(), "hex_identity_5")


class TestMatrixGrid(snapshottest.TestCase):
    # Not actually a class, but a grid with a numeric underlying list
    def setUp(self):
        self.initial_list = np.array(
            [
                [1, 0, 0],
                [0, 2, 0],
                [0, 0, 3],
                [0, 0, 4],
            ]
        )
        self.g = Grid(self.initial_list)

    def test_get_adjacent_coords(self):
        self.assertListEqual(self.g.get_adjacent_coords(0, 0), [(1, 0), (0, 1)])

        self.assertListEqual(
            self.g.get_adjacent_coords(1, 1), [(0, 1), (2, 1), (1, 0), (1, 2)]
        )

        self.assertListEqual(self.g.get_adjacent_coords(2, 2), [(1, 2), (2, 1), (2, 3)])

        self.assertListEqual(self.g.get_adjacent_coords(2, 3), [(1, 3), (2, 2)])


if __name__ == "__main__":
    unittest.main()
