"""
The workhorse of the tiled_tools library. This file contains the Grid class,
which is used to represent a grid of objects in the game. It was designed
with search in mind, but can also be used as a matrix for other purposes.
"""

from enum import Enum
from typing import Any

import numpy as np
from numpy.typing import ArrayLike


class GridType(Enum):
    """
    The type of a grid, square or hexagonal. This is used to determine
    the neighbors of a cell.
    """

    # A square grid
    TABLE = "table"
    # A hexagonal grid, where each cell has at most 6 neighbors
    HEX = "hex"


class WrapDirection(Enum):
    """
    The wrap direction of a grid. This is used to determine if the
    edges of the grid wrap around to the other side.
    """

    NONE = 0
    HORIZONTAL = 1
    VERTICAL = 2
    TORUS = 3  # Both horizontal and vertical


class Grid:
    """
    A grid of objects in the game.
    """

    def __init__(
        self,
        inital_list: ArrayLike,
        grid_type: GridType = GridType.TABLE,
        wrap_direction: WrapDirection = WrapDirection.NONE,
    ):
        """

        Args:
          inital_list (list): A list of lists of objects to initialize the grid with.
          Height and width are inferred from this list. There are no
          grid_type (GridType): The type of the grid. Default is GridType.TABLE.
          wrap_direction (WrapDirection): The wrap direction of the grid. Default is
          WrapDirection.NONE.
        """

        self.grid = np.array(inital_list)

        self.grid_width = len(inital_list[0])
        self.grid_height = len(inital_list)

        self.grid_type = grid_type
        self.wrap_direction = wrap_direction

    def get_grid_type(self) -> GridType:
        """
        Return the type of the grid.
        """
        return self.grid_type

    def get_wrap_direction(self) -> WrapDirection:
        """
        Return the wrap direction of the grid.
        """
        return self.wrap_direction

    def set_wrap_direction(self, wrap_direction: WrapDirection):
        """
        Set the wrap direction of the grid.
        """
        self.wrap_direction = wrap_direction

    def get_grid(self) -> np.ndarray:
        """
        Return the grid as a numpy array.
        """
        return self.grid

    def tolist(self) -> list:
        """
        Return the grid as a list of lists.
        """
        return [row.tolist() for row in self.grid]

    def copy(self) -> "Grid":
        """
        Return a copy of the grid.
        """
        return Grid(self.tolist(), self.grid_type, self.wrap_direction)

    @property
    def width(self) -> int:
        """
        Return the width of the grid.
        """
        return self.grid_width

    @property
    def height(self) -> int:
        """
        Return the height of the grid.
        """
        return self.grid_height

    def get(self, col: int, row: int) -> Any:
        """
        Get the value of a cell in the grid.

        Args:
            col (int): The column of the cell to get.
            row (int): The row of the cell to get.
        """
        return self.grid[row][col]

    def set(self, col: int, row: int, value: Any):
        """
        Set the value of a cell in the grid.

        Args:
            col (int): The column of the cell to set.
            row (int): The row of the cell to set.
            value (Any): The value to set the cell to.
        """
        self.grid[row][col] = value

    def get_row(self, row: int) -> list[Any]:
        """
        Return a list of values in a given row.
        """
        return self.grid[row].tolist()

    def get_col(self, col: int) -> list[Any]:
        """
        Return a list of values in a given column.
        """
        return self.grid[:, col].tolist()

    def set_row(self, row: int, values: list[Any]):
        """
        Set the values in a given row.
        """
        self.grid[row] = values

    def set_col(self, col: int, values: list[Any]):
        """
        Set the values in a given column.
        """
        self.grid[:, col] = values

    def get_adjacent(self, col: int, row: int) -> list[Any]:
        """
        Return a list of adjacent values to a given cell.
        """
        adjacent_coords = self.get_adjacent_coords(col, row)

        # Get the values at each coordinate
        return [self.get(c, r) for c, r in adjacent_coords]

    def get_adjacent_coords(self, col: int, row: int) -> list[tuple[int, int]]:
        """
        Return a list the adjacent coordinates to a given cell.
        """
        adjacent_coords = GridHelper.get_neighbor_coords(self.grid_type, col, row)

        # Filter out any coordinates that are out of bounds,
        # or wrap them around if needed
        return GridHelper.filter_coords(self, adjacent_coords)

    def __add__(self, other: "Grid") -> "Grid":
        """
        Add two Grids together.

        Args:
          other (Grid): The Grid to add to this one.
        """
        return Grid(self.grid + other.grid)

    def __sub__(self, other: "Grid") -> "Grid":
        """
        Subtract two Grids together.

        Args:
          other (Grid): The Grid to subtract from this one.
        """
        return Grid(self.grid - other.grid)

    def __mul__(self, other: "Grid") -> "Grid":
        """
        Multiply two Grids together.

        Args:
          other (Grid): The Grid to multiply this one by.
        """
        return Grid(np.matmul(self.grid, other.grid))

    def __eq__(self, other: "Grid") -> bool:
        """
        Check if two Grids are equal.

        Args:
          other (Grid): The Grid to compare this one to.
        """
        return np.array_equal(self.grid, other.grid)

    def __repr__(self):
        return str(self.grid)

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        return iter(self.grid)


class HexGrid(Grid):
    """
    An alias for a grid with the type GridType.HEX.
    """

    def __init__(
        self, inital_list: ArrayLike, wrap_direction: WrapDirection = WrapDirection.NONE
    ):
        super().__init__(inital_list, GridType.HEX, wrap_direction)


# pylint: disable=too-few-public-methods
class GridGenerator:
    """
    Helper methods for generating grids.
    """

    @staticmethod
    def identity(
        size: int,
        grid_type: GridType = GridType.TABLE,
        wrap_direction: WrapDirection = WrapDirection.NONE,
    ) -> Grid:
        """
        Return an identity grid of a given size.

        Args:
          size (int): The size of the grid to initialize.
        """
        grid = np.zeros((size, size))
        for i in range(size):
            grid[i][i] = 1

        return Grid(grid, grid_type, wrap_direction)


class GridHelper:
    """
    Useful methods for working with grids.
    """

    @staticmethod
    def get_neighbor_coords(grid_type: GridType, col: int, row: int):
        """
        Return a list of relative coordinates for a given grid type.
        """
        if grid_type == GridType.TABLE:
            return GridHelper.get_table_relative_coords(col, row)

        return GridHelper.get_hex_relative_coords(col, row)

    @staticmethod
    def get_table_relative_coords(col: int, row: int):
        """
        Return a list of relative coordinates for a grid.
        """
        return [
            (col - 1, row),  # Left
            (col + 1, row),  # Right
            (col, row - 1),  # Above
            (col, row + 1),  # Below
        ]

    @staticmethod
    def get_hex_relative_coords(col: int, row: int):
        """
        Return a list of relative coordinates for a hex grid.
        """
        odd_rel = [
            (col, row - 1),  # Above
            (col, row + 1),  # Below
            (col - 1, row),  # Upper left
            (col - 1, row + 1),  # Lower left
            (col + 1, row),  # Upper right
            (col + 1, row + 1),  # Lower right
        ]

        even_rel = [
            (col, row - 1),  # Above
            (col, row + 1),  # Below
            (col - 1, row - 1),  # Upper left
            (col - 1, row),  # Lower left
            (col + 1, row - 1),  # Upper right
            (col + 1, row),  # Lower right
        ]

        return odd_rel if col % 2 == 1 else even_rel

    @staticmethod
    def correct_adjacent_coord(grid: Grid, col: int, row: int) -> tuple[int, int]:
        """
        Correct any coordinates that are out of bounds,
        based on the wrap direction of the grid.

        Raises:
            AssertionError: If the grid has no wrap direction
        """
        assert (
            grid.wrap_direction != WrapDirection.NONE
        ), "Cannot correct adjacent coordinates for a grid with no wrap direction"

        if grid.wrap_direction in (WrapDirection.HORIZONTAL, WrapDirection.TORUS):
            # replace -1 col with width - 1, and width with 0
            if col == -1:
                col = grid.width - 1
            elif col == grid.width:
                col = 0

        if grid.wrap_direction in (WrapDirection.VERTICAL, WrapDirection.TORUS):
            # replace -1 row with height - 1, and height with 0
            if row == -1:
                row = grid.height - 1
            elif row == grid.height:
                row = 0

        return (col, row)

    @staticmethod
    def filter_coords(
        grid: Grid, coords: list[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        """
        Filter out any coordinates that are out of bounds.
        """
        if grid.wrap_direction == WrapDirection.NONE:
            return [
                (c, r)
                for c, r in coords
                if 0 <= c < grid.width and 0 <= r < grid.height
            ]

        return [GridHelper.correct_adjacent_coord(grid, c, r) for c, r in coords]
