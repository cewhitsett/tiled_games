import random
from enum import Enum
from typing import Optional

from src.tiled_tools.common.grid import Grid, WrapDirection
from src.tiled_tools.common.queues import Queue

from .map import ISLAND_RULESET, TileRuleSet, TileType


class QuantumState:
    """
    A wrapper around a tile type that represents the possible states
    remaining for a specific tile. It defaults to use the TileType enum,
    but can be used with any enum, trying to figure out the best way to get typing
    to work with this.
    """

    def __init__(self, tile_enum: TileType):
        self.tile_enum = tile_enum
        self.possible_states = [tile for tile in tile_enum]

    def collapse(self, tile: Enum):
        """
        Collapses the possible states to a single state
        """
        self.possible_states = [tile]

    def remove_state(self, tile: Enum):
        """
        Removes a state from the possible states
        """
        self.possible_states.remove(tile)

    def remove_contrary_states(self, tile: TileType, ruleset: TileRuleSet):
        """
        Removes states that are not allowed by the ruleset, given that a neighbor
        tile was observed to be of a certain type.
        """
        to_remove = []
        for state in self.possible_states:
            if not ruleset.is_allowed_neighbor(tile, state):
                to_remove.append(state)

        for state in to_remove:
            self.possible_states.remove(state)

    def __repr__(self):
        if len(self.possible_states) == 1:
            return f"QuantumState({self.possible_states[0].name})"

        names = ", ".join([f"{state.name}?" for state in self.possible_states])
        return f"QuantumState({names})"

    def __str__(self):
        return self.__repr__()


class WaveFunctionCollapse:
    """
    I started this whole project because of how interesting this
    algorithm is.
    """

    def __init__(
        self,
        ruleset: TileRuleSet,
        grid: Grid,
        desired_ratios: dict[TileType, float],
        neighbor_depth: int = 1,
    ):
        self.ruleset = ruleset
        self.grid = grid
        self.desired_ratios = desired_ratios
        self.neighbor_depth = neighbor_depth

    def collapse(self):
        """
        Runs the entire collapse algorithm until the grid is fully collapsed
        """
        uncollapsed = self.uncollapsed()

        while len(uncollapsed) > 0:
            c, r = self.random_uncollapsed()
            self.collapse_cell(c, r)
            self.propagate_collapse(c, r)
            self.remove_global_contrary_states()
            uncollapsed = self.uncollapsed()

    def collapse_cell(self, col: int, row: int):
        """
        Collapses a specific cell in the grid
        """
        cell = self.grid.get(col, row)
        remain_states = cell.possible_states
        observed = random.choice(remain_states)

        cell.collapse(observed)

    def remove_global_contrary_states(self):
        """
        This is not much of a problem on the 2D grid, but may be on
        hex grids. Will need to update it to resolve those issues.
        """
        pass

    def collapse_random(self) -> Optional[tuple[int, int]]:
        """
        Collapses a random tile in the grid. Returns the
        coordinates of the collapsed tile, or None if the grid
        is fully collapsed.
        """

        quantum_remaining = self.uncollapsed()

        if len(quantum_remaining) == 0:
            return None

        c, r = random.choice(list(quantum_remaining))
        cell = self.grid.get(c, r)
        remain_states = cell.possible_states
        observed = random.choice(remain_states)

        cell.collapse(observed)

        return c, r

    def propagate_collapse(self, col: int, row: int):
        """
        Propagates the collapse of a tile to its neighbors
        """
        visited = set()
        collapsing = Queue([(col, row)])

        while len(collapsing) > 0:
            to_collapsed = collapsing.pop()
            visited.add(to_collapsed)

            collapsed_cell = self.grid.get(*to_collapsed)

            for c, r in self.grid.get_adjacent_coords(*to_collapsed):
                if (c, r) in visited:
                    continue

                neighbor: QuantumState = self.grid.get(c, r)
                neighbor.remove_contrary_states(
                    collapsed_cell.possible_states[0], self.ruleset
                )

                if len(neighbor.possible_states) == 1:
                    collapsing.push((c, r))

    def uncollapsed(self) -> set[tuple[int, int]]:
        """
        Returns the set of uncollapsed cells in the grid
        """

        uncollapsed = set()

        for r in range(self.grid.height):
            for c in range(self.grid.width):
                if len(self.grid.get(c, r).possible_states) > 1:
                    uncollapsed.add((c, r))

        return uncollapsed

    def random_uncollapsed(self) -> tuple[int, int]:
        """
        Returns the coordinates of a random uncollapsed cell
        """

        uncollapsed = self.uncollapsed()

        return random.choice(list(uncollapsed))
