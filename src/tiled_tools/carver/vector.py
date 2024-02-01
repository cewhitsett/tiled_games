"""
Helpful class for Vector and matrix operations.
"""


from typing import Union

import numpy as np

from src.tiled_tools.common.custom_typing import AnyNumber, is_numeric


class Vector:
    """
    A wrapper for numpy arrays that provides useful vector operations.
    """

    def __init__(self, initial_list: list[AnyNumber]):
        """
        Initialize a Vector object, given a list

        Args:
          initial_list (list): A list of AnyNumbers to initialize the vector with.
        """
        self.vector = np.array(initial_list)

    def magnitude(self) -> AnyNumber:
        """
        Return the magnitude of the vector.
        """
        return np.sqrt(self.dot(self))

    def normalize(self) -> "Vector":
        """
        Normalize the vector.
        """
        return Vector(self.vector / self.magnitude())

    def dot(self, other: "Vector") -> AnyNumber:
        """
        Return the dot product of the vector with another vector.

        Args:
          other (Vector): The vector to dot this one with.
        """
        return np.dot(self.vector, other.vector)

    def dimension(self) -> int:
        """
        Return the length of the vector.
        """
        return len(self.vector)

    def __getitem__(self, index: int) -> AnyNumber:
        """
        Get an item from the vector.

        Args:
          index (int): The index of the item to get.
        """
        return self.vector[index]

    def __setitem__(self, index: int, value: AnyNumber):
        """
        Set an item in the vector.

        Args:
          index (int): The index of the item to set.
          value (AnyNumber): The value to set the item to.
        """
        self.vector[index] = value

    def __repr__(self) -> str:
        """
        Return a string representation of the vector.
        """
        return f"Vector({self.vector.tolist()})"

    def __str__(self) -> str:
        """
        Return a string representation of the vector.
        """
        return f"Vector({self.vector.tolist()})"

    def __add__(self, other: Union["Vector", AnyNumber]) -> "Vector":
        """
        Add two vectors together.

        Args:
          other (Vector|AnyNumber): The vector or scalar to add to this one.
        """
        if is_numeric(other):
            return Vector(self.vector + other)

        return Vector(self.vector + other.vector)

    def __sub__(self, other: Union["Vector", AnyNumber]) -> "Vector":
        """
        Subtract two vectors.

        Args:
          other (Vector): The vector or scalar to subtract from this one.
        """
        if is_numeric(other):
            return Vector(self.vector - other)

        return Vector(self.vector - other.vector)

    def __mul__(self, other: Union["Vector", AnyNumber]) -> Union["Vector", AnyNumber]:
        """
        Multiply the vector by a vector or a scalar. If multiplying by a vector,
        the dot product is returned.

        Args:
          other (Vector): The vector or scalar to multiply this one by.
        """
        if is_numeric(other):
            return Vector(self.vector * other)

        return float(self.dot(other))

    def __truediv__(self, other: Union["Vector", AnyNumber]) -> "Vector":
        """
        Divide the vector by a vector or a scalar.

        Args:
          other (Vector): The vector or scalar to divide this one by.
        """
        if is_numeric(other):
            return Vector(self.vector / other)

        return Vector(self.vector / other.vector)

    def __floordiv__(self, other: Union["Vector", AnyNumber]) -> "Vector":
        """
        Floor divide the vector by a vector or a scalar.

        Args:
          other (Vector): The vector or scalar to floor divide this one by.
        """
        if is_numeric(other):
            return Vector(self.vector // other)

        return Vector(self.vector // other.vector)

    def angle_between(self, other: "Vector") -> AnyNumber:
        """
        Return the angle between this vector and another vector.

        Args:
          other (Vector): The vector to calculate the angle to.
        """
        return np.arccos(self.dot(other) / (self.magnitude() * other.magnitude()))

    def __eq__(self, other: Union["Vector", list[AnyNumber]]) -> bool:
        """
        Check if two vectors are equal.

        Args:
          other (Vector|list): The vector or list to compare this one to.
        """
        if isinstance(other, Vector):
            return np.array_equal(self.vector, other.vector)

        return np.array_equal(self.vector, np.array(other))

    def tolist(self) -> list[AnyNumber]:
        """
        Return the vector as a list.
        """
        return self.vector.tolist()

    def __len__(self) -> int:
        """
        Return the length of the vector.
        """
        return len(self.vector)


class VectorGenerator:
    """
    Static class for generating vectors, for convenience.
    """

    @staticmethod
    def empty_vector(size: int):
        """
        Return an empty vector of a given size.

        Args:
          size (int): The size of the vector to initialize.
        """
        return Vector(np.zeros(size))

    @staticmethod
    def random_vector(size: int, min_value: AnyNumber = 0, max_value: AnyNumber = 1):
        """
        Return a random vector of a given size with values between min and max.

        Args:
          size (int): The size of the vector to initialize.
          min (AnyNumber): The minimum value of the vector. Default is 0.
          max (AnyNumber): The maximum value of the vector. Default is 1.
        """
        return Vector(np.random.uniform(min_value, max_value, size))
