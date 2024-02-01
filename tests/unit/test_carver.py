# pylint: disable=missing-docstring

import unittest

import numpy as np

from src.tiled_tools.carver.vector import Vector, VectorGenerator


class TestVector(unittest.TestCase):
    def setUp(self):
        pass

    def test_str(self):
        v = Vector([1, 2, 3])
        self.assertEqual(str(v), "Vector([1, 2, 3])")

    def test_init(self):
        initial_list = [1, 2, 3]
        v = Vector(initial_list)
        self.assertListEqual(v.tolist(), initial_list)

    def test_magnitude(self):
        initial_list = [1, 2, 3]
        v = Vector(initial_list)
        self.assertEqual(v.magnitude(), np.sqrt(14))

        v2 = Vector([3, 4])
        self.assertEqual(v2.magnitude(), 5)

    def test_normalize(self):
        initial_list = [1, 2, 3]
        v = Vector(initial_list)
        self.assertEqual(v.magnitude(), np.sqrt(14))

        normalized_vector = v.normalize()
        self.assertTrue(np.isclose(normalized_vector.magnitude(), 1.0))

    def test_dot(self):
        v1 = Vector([1, 2, 3])
        v2 = Vector([4, 5, 6])
        self.assertEqual(v1.dot(v2), 32)

        v3 = Vector([7, 8, 9, -1])
        v4 = Vector([10, 11, 12, -2])
        self.assertEqual(v3.dot(v4), 268)

    def test_dimension(self):
        v1 = Vector([1, 2, 3])
        self.assertEqual(v1.dimension(), 3)

        v2 = Vector([4, 5, 6, 7, 8])
        self.assertEqual(v2.dimension(), 5)

        empty = Vector([])
        self.assertEqual(empty.dimension(), 0)

    def test_getitem(self):
        v = Vector([1, 2, -62])

        self.assertEqual(v[0], 1)
        self.assertEqual(v[1], 2)
        self.assertEqual(v[2], -62)

    def test_setitem(self):
        v = Vector([1, 2, -62])
        v[0] = 0
        v[1] = 1
        v[2] = 2

        self.assertEqual(v[0], 0)
        self.assertEqual(v[1], 1)
        self.assertEqual(v[2], 2)

    def test_repr(self):
        v = Vector([20, 2, -12])
        self.assertEqual(repr(v), "Vector([20, 2, -12])")

    def test_add(self):
        v1 = Vector([1, 2, 3])
        v2 = Vector([4, 5, 6])
        v3 = v1 + v2
        self.assertListEqual(v3.tolist(), [5, 7, 9])

        v4 = v1 + 10

        self.assertListEqual(v4.tolist(), [11, 12, 13])

    def test_sub(self):
        v1 = Vector([9, -8, 3])
        v2 = Vector([4, 5, 6])
        v3 = v1 - v2
        self.assertListEqual(v3.tolist(), [5, -13, -3])

        v4 = v1 - 10
        self.assertListEqual(v4.tolist(), [-1, -18, -7])

    def test_mul(self):
        v1 = Vector([1, 2, 3])
        v2 = Vector([4, 5, 6])
        dot_prod = v1 * v2
        self.assertEqual(dot_prod, 32)

        v3 = v1 * 10
        self.assertListEqual(v3.tolist(), [10, 20, 30])

    def test_div(self):
        v1 = Vector([-121, 2200, -30])
        v2 = Vector([-4, -5, 6])
        v3 = v1 / v2
        self.assertListEqual(v3.tolist(), [30.25, -440, -5])

        v4 = v1 / 10
        self.assertListEqual(v4.tolist(), [-12.1, 220, -3])

    def test_floor_div(self):
        v1 = Vector([-123, 2204, -35])
        v2 = Vector([-4, -5, 6])
        v3 = v1 // v2
        self.assertListEqual(v3.tolist(), [30, -441, -6])

        v4 = v1 // 10
        self.assertListEqual(v4.tolist(), [-13, 220, -4])

    def test_sum(self):
        v1 = Vector([1, 2, 3])
        v2 = Vector([4, 5, 6])
        v3 = Vector([7, 8, 9])

        self.assertEqual(sum(v1), 6)
        self.assertEqual(sum(v2), 15)
        self.assertEqual(sum(v3), 24)

    def test_angle_between(self):
        v1 = Vector([1, 0, 0])
        v2 = Vector([0, 1, 0])
        self.assertAlmostEqual(v1.angle_between(v2), np.pi / 2)

        v3 = Vector([0, 0, 1])
        self.assertAlmostEqual(v1.angle_between(v3), np.pi / 2)

        v4 = Vector([1, 1, 0])
        self.assertAlmostEqual(v1.angle_between(v4), np.pi / 4)

        v5 = Vector([1, 1, 1])
        self.assertAlmostEqual(v1.angle_between(v5), np.arccos(1 / np.sqrt(3)))

    def test_eq(self):
        v1 = Vector([1, 2, 3])
        v2 = Vector([1, 2, 3])
        self.assertEqual(v1, v2)

        v3 = Vector([4, 5, 6])
        self.assertNotEqual(v1, v3)

        self.assertEqual(v3, [4, 5, 6])


class TestVectorGenerator(unittest.TestCase):
    def setUp(self):
        pass

    def test_empty_vector(self):
        v = VectorGenerator.empty_vector(3)
        assert v.dimension() == 3
        assert np.array_equal(v.vector, np.array([0, 0, 0]))

        v = VectorGenerator.empty_vector(10)
        assert v.dimension() == 10
        assert np.array_equal(v.vector, np.array([0] * 10))

    def test_random_vector(self):
        v = VectorGenerator.random_vector(3)
        assert v.dimension() == 3
        assert v.magnitude() > 0


if __name__ == "__main__":
    unittest.main()
