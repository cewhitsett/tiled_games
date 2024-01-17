"""
This file will hold services and functionality around
dimensions and measurements in the game.
"""

from numbers import Number


class Size:
    """
    A size in the game. Base unit does not matter, but assume inches

    Args:
      width (Number): The width of the size.
      height (Number): The height of the size.
      depth (Number): The depth of the size. Defaults to 1, which is a 2D size.
    """

    def __init__(self, width: Number, height: Number, depth: Number = 1):
        self.width: Number = width
        self.height: Number = height
        self.depth: Number = depth

    def area(self) -> Number:
        """
        Return the area of the size, assuming 2D.
        """
        return self.width * self.height

    def volume(self) -> Number:
        """
        Return the volume of the size.
        """
        return self.width * self.height * self.depth

    def __str__(self) -> str:
        return f"Size({self.width}, {self.height}, {self.depth})"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: "Size") -> bool:
        return (
            self.width == other.width
            and self.height == other.height
            and self.depth == other.depth
        )
