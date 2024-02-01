# pylint: disable=missing-docstring

import unittest

from src.tiled_tools.common.graph import Edge, Graph, Node


class TestNode(unittest.TestCase):
    def setUp(self):
        self.n = Node([1, 2, 3], "node")

    def test_str(self):
        self.assertEqual(str(self.n), "Node([1, 2, 3], node)")

    def test_eq(self):
        n2 = Node([1, 2, 3])
        self.assertEqual(self.n, n2)

        n3 = Node([4, 5, 6])
        self.assertNotEqual(self.n, n3)


class TestEdge(unittest.TestCase):
    def setUp(self):
        self.n1 = Node([1, 2, 3], "n1")
        self.n2 = Node([4, 5, 6], "n2")
        self.e = Edge(self.n1, self.n2, 5)

        self.edge = Edge(self.n1, self.n1, 5, "edge")

    def test_str(self):
        self.assertEqual(
            str(self.edge), "Edge(Node([1, 2, 3], n1), Node([1, 2, 3], n1), 5, edge)"
        )

        self.assertEqual(self.e.length, 5)
        self.assertTrue(any(self.e.id))


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.n1 = Node([1, 2, 3], "n1")
        self.n2 = Node([4, 5, 6], "n2")
        self.e = Edge(self.n1, self.n2, 5, "prt")

        self.graph = Graph()
        self.graph.add_edge(self.e)

    def test_get_edge(self):
        self.assertEqual(self.graph.get_edge("prt"), self.e)

    def test_get_edges(self):
        self.assertEqual(self.graph.get_edges(self.n1), [self.e])
        self.assertEqual(self.graph.get_edges(self.n2), [self.e])

    def test_get_nodes(self):
        self.assertEqual(self.graph.get_nodes(), {self.n1, self.n2})

    def test_get_node(self):
        self.assertEqual(self.graph.get_node("n1"), self.n1)
        self.assertEqual(self.graph.get_node("n2"), self.n2)


if __name__ == "__main__":
    unittest.main()
