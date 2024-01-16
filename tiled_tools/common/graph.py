from numbers import Number
from typing import Optional
import numpy as np

from .constants import ALPHABET, ID_SIZE


class Node:
    """
    A node is a point in a graph.
    """

    def __init__(self, value=None, id: str = ""):
        if id == "":
            self.id = "".join(np.random.choice(ALPHABET, size=ID_SIZE))
        else:
            self.id = id

        self.value = value

    def __str__(self):
        return f"Node({self.value}, {self.id})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other: "Node"):
        return self.value == other.value

    def __hash__(self):
        return hash(self.id)


class Edge:
    """
    An edge is a connection between two nodes.
    """

    def __init__(
        self, node1: Node, node2: Optional[Node], length: Number, id: str = ""
    ):
        if id == "":
            self.id = np.random.choice(ALPHABET, size=ID_SIZE)
        else:
            self.id = id

        self.node1 = node1
        self.node2 = node2
        self.length = length

    def __str__(self):
        return f"Edge({self.node1}, {self.node2}, {self.length}, {self.id})"

    def __repr__(self):
        return str(self)


class Graph:
    """
    A graph is a collection of nodes and edges.
    """

    def __init__(self):
        self.edges: dict[tuple[Node, Node], Edge] = {}

    def add_edge(self, edge: Edge):
        """
        Add an edge to the graph.
        """
        self.edges[(edge.node1, edge.node2)] = edge
        self.edges[(edge.node2, edge.node1)] = edge

    def get_edge(self, node1: Node, node2: Node) -> Optional[Edge]:
        """
        Get an edge between two nodes.
        """
        return self.edges.get((node1, node2), None)

    def get_edges(self, node: Node) -> list[Edge]:
        """
        Get all edges connected to a node.
        """
        return [
            edge
            for edge in self.edges.values()
            if edge.node1 == node or edge.node2 == node
        ]

    def get_nodes(self) -> list[Node]:
        """
        Get all nodes in the graph.
        """
        return list(
            set(
                [
                    node
                    for edge in self.edges.values()
                    for node in [edge.node1, edge.node2]
                ]
            )
        )

    def get_node(self, id: str) -> Optional[Node]:
        """
        Get a node by its id.
        """
        return next((node for node in self.get_nodes() if node.id == id), None)

    def get_neighbors(self, node: Node) -> list[Node]:
        """
        Get all neighbors of a node.
        """
        return [
            edge.node2
            for edge in self.get_edges(node)
            if edge.node1 == node or edge.node2 == node
        ]
