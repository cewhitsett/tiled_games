"""
This file will hold services and functionality around
dimensions and measurements in the game.
"""

from tiled_tools.common.custom_typing import AnyNumber


class Size:
    """
    A size in the game. Base unit does not matter, but assume inches

    Args:
      width (AnyNumber): The width of the size.
      height (AnyNumber): The height of the size.
      depth (AnyNumber): The depth of the size. Defaults to 1, which is a 2D size.
    """

    def __init__(self, width: AnyNumber, height: AnyNumber, depth: AnyNumber = 1):
        self.width: AnyNumber = width
        self.height: AnyNumber = height
        self.depth: AnyNumber = depth

    def area(self) -> AnyNumber:
        """
        Return the area of the size, assuming 2D.
        """
        return self.width * self.height

    def volume(self) -> AnyNumber:
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
