from enum import Enum
from numbers import Number
from typing import Any
import numpy as np
from numpy.typing import ArrayLike


class GridType(Enum):
    # A square grid
    TABLE = "table"
    # A hexagonal grid, where each cell has at most 6 neighbors
    HEX = "hex"


class WrapDirection(Enum):
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
          inital_list (list): A list of lists of objects to initialize the grid with. Height and width are inferred from this list. There are no
          grid_type (GridType): The type of the grid. Default is GridType.TABLE.
          wrap_direction (WrapDirection): The wrap direction of the grid. Default is WrapDirection.NONE.
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
        return self.grid[row][col]

    def set(self, col: int, row: int, value):
        self.grid[row][col] = value

    def get_adjacent(self, col: int, row: int) -> list[Any]:
        """
        Return a list of adjacent cells to a given cell.
        """
        adjacent_coords = self.get_adjacent_coords(col, row)

        # Get the values at each coordinate
        return [self.get(c, r) for c, r in adjacent_coords]

    def get_adjacent_coords(self, col: int, row: int) -> list[tuple[int, int]]:
        """
        Return a list of adjacent cells to a given cell.
        """
        adjacent_coords = GridHelper.get_neighbor_coords(self.grid_type, col, row)

        # Filter out any coordinates that are out of bounds, or wrap them around if needed
        return GridHelper.filter_coords(self, adjacent_coords)

    def __getitem__(self, index: tuple[int, int]) -> Any:
        """
        Returns the item at the given index.

        Args:
          index (tuple[int, int]): The item to get, in the for col, row
        """
        return self.grid[index[1]][index[0]]

    def __setitem__(self, index: tuple[int, int], value):
        """
        Sets the item at the given index.

        Args:
          index (tuple[int, int]): The item to set, in the for col, row
        """
        self.grid[index[1]][index[0]] = value

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

    def __str__(self):
        return str(self.grid)

    def __repr__(self):
        return str(self)


class HexGrid(Grid):
    """
    An alias for a grid with the type GridType.HEX.
    """

    def __init__(
        self, inital_list: ArrayLike, wrap_direction: WrapDirection = WrapDirection.NONE
    ):
        super().__init__(inital_list, GridType.HEX, wrap_direction)


class GridGenerator:
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
        elif grid_type == GridType.HEX:
            return GridHelper.get_hex_relative_coords(col, row)
        else:
            raise ValueError(f"Unknown grid type {grid_type}")

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
    def get_matrix_relative_coords(col: int, row: int):
        """
        Return a list of relative coordinates for a matrix grid, which is the same as a grid.
        """
        GridHelper.get_table_relative_coords(col, row)

    @staticmethod
    def correct_adjacent_coord(grid: Grid, col: int, row: int) -> tuple[int, int]:
        """
        Correct any coordinates that are out of bounds, based on the wrap direction of the grid.
        """
        assert (
            grid.wrap_direction != WrapDirection.NONE
        ), "Cannot correct adjacent coordinates for a grid with no wrap direction"

        if (
            grid.wrap_direction == WrapDirection.HORIZONTAL
            or grid.wrap_direction == WrapDirection.TORUS
        ):
            # replace -1 col with width - 1, and width with 0
            if col == -1:
                col = grid.width - 1
            elif col == grid.width:
                col = 0

        if (
            grid.wrap_direction == WrapDirection.VERTICAL
            or grid.wrap_direction == WrapDirection.TORUS
        ):
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
