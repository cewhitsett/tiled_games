# pylint: disable=missing-docstring

import unittest

from src.tiled_tools.carver.measurements import Size


class TestSize(unittest.TestCase):
    def test_init(self):
        size = Size(1, 2, 3)
        self.assertEqual(size.width, 1)
        self.assertEqual(size.height, 2)
        self.assertEqual(size.depth, 3)

    def test_area(self):
        size = Size(7.5, 2, 3)
        self.assertEqual(size.area(), 15)

    def test_volume(self):
        size = Size(8, 4, 2)
        self.assertEqual(size.volume(), 64)

    def test_str(self):
        size = Size(1, 2, 3)
        self.assertEqual(str(size), "Size(1, 2, 3)")

    def test_repr(self):
        size = Size(1, 2, 3)
        self.assertEqual(repr(size), "Size(1, 2, 3)")

    def test_eq(self):
        size1 = Size(1, 2, 3)
        size2 = Size(1, 2, 3)
        self.assertEqual(size1, size2)

        size3 = Size(1, 2, 4)
        self.assertNotEqual(size1, size3)
