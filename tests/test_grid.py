# pylint: disable=missing-docstring

import unittest

import numpy as np

from tiled_tools.common.grid import (
    Grid,
    GridGenerator,
    GridType,
    HexGrid,
    WrapDirection,
)


class TestGrid(unittest.TestCase):
    def setUp(self):
        self.initial_list = [[None for _ in range(3)] for _ in range(4)]
        self.g = Grid(self.initial_list, wrap_direction=WrapDirection.NONE)

    def test_copy(self):
        self.g.set(0, 0, 1)
        self.g.set(1, 1, 2)
        self.g.set(2, 2, 3)
        self.g.set(2, 3, 4)

        copy = self.g.copy()

        self.assertEqual(copy.get(0, 0), 1)
        self.assertEqual(copy.get(1, 1), 2)
        self.assertEqual(copy.get(2, 2), 3)
        self.assertEqual(copy.get(2, 3), 4)

        self.assertEqual(copy.get_grid_type(), GridType.TABLE)
        self.assertEqual(copy.get_wrap_direction(), WrapDirection.NONE)

        self.assertEqual(copy, copy.copy())

    def test_grid_type(self):
        self.assertEqual(self.g.get_grid_type(), GridType.TABLE)

    def test_wrap_direction(self):
        self.assertEqual(self.g.get_wrap_direction(), WrapDirection.NONE)

    def test_set_wrap_direction(self):
        self.g.set_wrap_direction(WrapDirection.HORIZONTAL)
        self.assertEqual(self.g.get_wrap_direction(), WrapDirection.HORIZONTAL)

    def test_get_grid(self):
        self.assertListEqual(self.g.get_grid().tolist(), self.initial_list)

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

    def test_tolist(self):
        self.g.set(0, 0, 1)
        self.g.set(1, 1, 2)
        self.g.set(2, 2, 3)
        self.g.set(2, 3, 4)

        self.assertListEqual(
            self.g.tolist(),
            [
                [1, None, None],
                [None, 2, None],
                [None, None, 3],
                [None, None, 4],
            ],
        )

    def test_add(self):
        identity = GridGenerator.identity(3)
        other = Grid(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

        self.assertEqual(
            (identity + other).tolist(), [[2, 2, 3], [4, 6, 6], [7, 8, 10]]
        )

    def test_sub(self):
        identity = GridGenerator.identity(3)
        other = Grid(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

        self.assertEqual(
            (identity - other).tolist(), [[0, -2, -3], [-4, -4, -6], [-7, -8, -8]]
        )

    def test_mul(self):
        identity = GridGenerator.identity(3)

        self.assertEqual((identity * identity).tolist(), identity.tolist())

    def test_eq(self):
        identity = GridGenerator.identity(3)
        other = Grid(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
        base_identity = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

        self.assertEqual(identity, identity)
        self.assertNotEqual(identity, other)
        self.assertEqual(identity, Grid(base_identity))

    def test_str(self):
        identity = GridGenerator.identity(3)
        self.assertEqual(str(identity), "[[1. 0. 0.]\n [0. 1. 0.]\n [0. 0. 1.]]")

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

        self.assertEqual(self.g.grid[0][0], 1)
        self.assertEqual(self.g.grid[1][1], 2)
        self.assertEqual(self.g.grid[2][2], 3)
        self.assertEqual(self.g.grid[3][2], 4)

    def test_get_adjacent_coords(self):
        identity = GridGenerator.identity(3)

        self.assertListEqual(identity.get_adjacent_coords(0, 0), [(1, 0), (0, 1)])

        self.assertListEqual(
            identity.get_adjacent_coords(1, 1), [(0, 1), (2, 1), (1, 0), (1, 2)]
        )

        self.assertListEqual(identity.get_adjacent_coords(2, 2), [(1, 2), (2, 1)])

        wrapped = GridGenerator.identity(3, wrap_direction=WrapDirection.TORUS)
        self.assertListEqual(
            wrapped.get_adjacent_coords(0, 0), [(2, 0), (1, 0), (0, 2), (0, 1)]
        )

        self.assertListEqual(
            wrapped.get_adjacent_coords(2, 2), [(1, 2), (0, 2), (2, 1), (2, 0)]
        )

    def test_get_adjacent(self):
        identity = GridGenerator.identity(3)

        self.assertListEqual(identity.get_adjacent(0, 0), [0, 0])

        self.assertListEqual(identity.get_adjacent(1, 1), [0, 0, 0, 0])

        self.assertListEqual(identity.get_adjacent(2, 2), [0, 0])

        self.assertListEqual(identity.get_adjacent(1, 0), [1, 0, 1])


class TestHexGrid(unittest.TestCase):
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

    def test_get_adjacent(self):
        grid = GridGenerator.identity(4, GridType.HEX, WrapDirection.TORUS)

        self.assertListEqual(grid.get_adjacent(0, 0), [0.0, 0.0, 1.0, 0.0, 0.0, 0.0])
        self.assertListEqual(grid.get_adjacent(1, 1), [0.0, 0.0, 0.0, 0.0, 0.0, 1.0])
        self.assertListEqual(grid.get_adjacent(2, 2), [0.0, 0.0, 1.0, 0.0, 0.0, 0.0])
        self.assertListEqual(grid.get_adjacent(1, 0), [0.0, 1.0, 1.0, 0.0, 0.0, 0.0])


class TestGridGenerator(unittest.TestCase):
    def setUp(self):
        pass

    # TODO: replace snapshots with new library
    def test_identity(self):
        identity = GridGenerator.identity(3)
        self.assertEqual(type(identity), Grid)
        # self.assertMatchSnapshot(identity.tolist(), "grid_identity_3")

        identity = GridGenerator.identity(5, GridType.HEX)
        self.assertEqual(type(identity), Grid)
        # self.assertMatchSnapshot(identity.tolist(), "hex_identity_5")


class TestMatrixGrid(unittest.TestCase):
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
