"""
Classes, services and functions for working with graphs,
nodes and edges.
"""

from typing import Optional

import numpy as np

from src.tiled_tools.common.custom_typing import AnyNumber

from .constants import ALPHABET, ID_SIZE


class Node:
    """
    A node is a point in a graph.
    """

    def __init__(self, value=None, ident: str = ""):
        # This is helpful for search, but not necessary and there are no
        # restrictions on the ID being unique if you set it yourself.
        if ident == "":
            self._id = "".join(np.random.choice(ALPHABET, size=ID_SIZE))
        else:
            self._id = ident

        self.value = value

    @property
    def id(self) -> str:
        """
        Unique identifier for the node, for use in search.
        """
        return self._id

    def __repr__(self) -> str:
        return f"Node({self.value}, {self.id})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other: "Node"):
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.id)


class Edge:
    """
    An edge is a connection between two nodes.
    """

    def __init__(
        self, node1: Node, node2: Optional[Node], length: AnyNumber, ident: str = ""
    ):
        if ident == "":
            self._id = np.random.choice(ALPHABET, size=ID_SIZE)
        else:
            self._id = ident

        self.node1 = node1
        self.node2 = node2
        self.length = length

    @property
    def id(self) -> str:
        """
        Unique identifier for the edge, for use in search.
        """
        return self._id

    def __repr__(self) -> str:
        return f"Edge({self.node1}, {self.node2}, {self.length}, {self.id})"

    def __str__(self):
        return self.__repr__()

    def __hash__(self) -> int:
        sorted_ids = sorted([self.node1.id, self.node2.id])
        return hash((sorted_ids[0], sorted_ids[1]))


class Graph:
    """
    A graph is a collection of nodes and edges.
    """

    def __init__(self):
        self.edges: set[Edge] = set([])

    def add_edge(self, edge: Edge):
        """
        Add an edge to the graph.
        """
        self.edges.add(edge)

    def get_edges(self, node: Node) -> list[Edge]:
        """
        Get all edges connected to a node.
        """
        return [edge for edge in self.edges if node in (edge.node1, edge.node2)]

    def get_edge(self, ident: str) -> Optional[Edge]:
        """
        Get an edge by its id, if it exists.
        """
        return next((edge for edge in self.edges if edge.id == ident), None)

    def get_nodes(self) -> set[Node]:
        """
        Get all nodes in the graph.
        """
        all_nodes = set(
            node for edge in self.edges for node in [edge.node1, edge.node2]
        )

        return all_nodes

    def get_node(self, ident: str) -> Optional[Node]:
        """
        Get a node by its id.
        """
        return next((node for node in self.get_nodes() if node.id == ident), None)

    def get_neighbors(self, node: Node) -> list[Node]:
        """
        Get all neighbors of a node.
        """
        return [
            edge.node2
            for edge in self.get_edges(node)
            if node in (edge.node1, edge.node2)
        ]
