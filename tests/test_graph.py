import snapshottest
from tiled_tools.common.graph import Edge, Node


class TestNode(snapshottest.TestCase):
    def setUp(self):
        self.n = Node([1, 2, 3], "node")

    def test_str(self):
        self.assertEqual(str(self.n), "Node([1, 2, 3], node)")

    def test_eq(self):
        n2 = Node([1, 2, 3])
        self.assertEqual(self.n, n2)

        n3 = Node([4, 5, 6])
        self.assertNotEqual(self.n, n3)


class TestEdge(snapshottest.TestCase):
    def setUp(self):
        self.n1 = Node([1, 2, 3])
        self.n2 = Node([4, 5, 6])
        self.e = Edge(self.n1, self.n2, 5)

        self.self_edge = Edge(self.n1, self.n1, 5, "edge")


if __name__ == "__main__":
    import unittest

    unittest.main()
