"""
Helpful class for Vector and matrix operations.
"""

from numbers import Number
from typing import Union

import numpy as np


class Vector:
    """
    A wrapper for numpy arrays that provides useful vector operations.
    """

    def __init__(self, initial_list: list[Number]):
        """
        Initialize a Vector object, given a list

        Args:
          initial_list (list): A list of numbers to initialize the vector with.
        """
        self.vector = np.array(initial_list)

    def magnitude(self) -> Number:
        """
        Return the magnitude of the vector.
        """
        return np.sqrt(self.dot(self))

    def normalize(self) -> "Vector":
        """
        Normalize the vector.
        """
        return Vector(self.vector / self.magnitude())

    def dot(self, other: "Vector") -> Number:
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

    def __getitem__(self, index: int) -> Number:
        """
        Get an item from the vector.

        Args:
          index (int): The index of the item to get.
        """
        return self.vector[index]

    def __setitem__(self, index: int, value: Number):
        """
        Set an item in the vector.

        Args:
          index (int): The index of the item to set.
          value (Number): The value to set the item to.
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

    def __add__(self, other: Union["Vector", Number]) -> "Vector":
        """
        Add two vectors together.

        Args:
          other (Vector|Number): The vector or scalar to add to this one.
        """
        if isinstance(other, Number):
            return Vector(self.vector + other)

        return Vector(self.vector + other.vector)

    def __sub__(self, other: Union["Vector", Number]) -> "Vector":
        """
        Subtract two vectors.

        Args:
          other (Vector): The vector or scalar to subtract from this one.
        """
        if isinstance(other, Number):
            return Vector(self.vector - other)

        return Vector(self.vector - other.vector)

    def __mul__(self, other: Union["Vector", Number]) -> Union["Vector", Number]:
        """
        Multiply the vector by a vector or a scalar. If multiplying by a vector,
        the dot product is returned.

        Args:
          other (Vector): The vector or scalar to multiply this one by.
        """
        if isinstance(other, Number):
            return Vector(self.vector * other)

        return float(self.dot(other))

    def __truediv__(self, other: Union["Vector", Number]) -> "Vector":
        """
        Divide the vector by a vector or a scalar.

        Args:
          other (Vector): The vector or scalar to divide this one by.
        """
        if isinstance(other, Number):
            return Vector(self.vector / other)

        return Vector(self.vector / other.vector)

    def __floordiv__(self, other: Union["Vector", Number]) -> "Vector":
        """
        Floor divide the vector by a vector or a scalar.

        Args:
          other (Vector): The vector or scalar to floor divide this one by.
        """
        if isinstance(other, Number):
            return Vector(self.vector // other)

        return Vector(self.vector // other.vector)

    def angle_between(self, other: "Vector") -> Number:
        """
        Return the angle between this vector and another vector.

        Args:
          other (Vector): The vector to calculate the angle to.
        """
        return np.arccos(self.dot(other) / (self.magnitude() * other.magnitude()))

    def __eq__(self, other: Union["Vector", list[Number]]) -> bool:
        """
        Check if two vectors are equal.

        Args:
          other (Vector|list): The vector or list to compare this one to.
        """
        if isinstance(other, Vector):
            return np.array_equal(self.vector, other.vector)

        return np.array_equal(self.vector, np.array(other))

    def tolist(self) -> list[Number]:
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
    def random_vector(size: int, min_value: Number = 0, max_value: Number = 1):
        """
        Return a random vector of a given size with values between min and max.

        Args:
          size (int): The size of the vector to initialize.
          min (Number): The minimum value of the vector. Default is 0.
          max (Number): The maximum value of the vector. Default is 1.
        """
        return Vector(np.random.uniform(min_value, max_value, size))


class Point:
    """
    A point in space
    """

    def __init__(self, initial_list: list[Number]):
        """
        Initialize a Point object, given a list

        Args:
          initial_list (list): A list of numbers to initialize the point with.
        """
        self.vector: Vector = Vector(initial_list)

    def distance(self, other: "Point") -> Number:
        """
        Return the distance between this point and another point.

        Args:
          other (Point): The point to calculate the distance to.
        """
        return (self.vector - other.vector).magnitude()

    def scale(self, scalar: Number) -> "Point":
        """
        Scale the point by a scalar.

        Args:
          scalar (Number): The scalar to scale the point by.
        """
        return Point((self.vector * scalar).tolist())

    def tolist(self) -> list[Number]:
        """
        Return the point as a list.
        """
        # v_list: list[Number] = self.vector.tolist()
        # print("UUU")
        # print(v_list)
        # return v_list
        return self.vector.tolist()

    def __getitem__(self, index: int) -> Number:
        """
        Get an item from the point.

        Args:
          index (int): The index of the item to get.
        """
        return self.vector[index]

    def __setitem__(self, index: int, value: Number):
        """
        Set an item in the point.

        Args:
          index (int): The index of the item to set.
          value (Number): The value to set the item to.
        """
        self.vector[index] = value

    def __add__(self, other: Union["Point", Vector]) -> "Point":
        """
        Add a vector or point to a point.

        Args:
          other (Point|Vector): The vector or point to add to this one.
        """
        if isinstance(other, Point):
            return Point([self.vector[i] + other.vector[i] for i in range(0, 3)])

        return Point(Vector(self.vector) + other)

    def __sub__(self, other: Union["Point", Vector]) -> "Point":
        """
        Subtract a vector or point from a point.

        Args:
          other (Point|Vector): The vector or point to subtract from this one.
        """
        if isinstance(other, Point):
            return Point(
                [self.vector[i] - other.vector[i] for i in range(self.dimension())]
            )

        return Point(self.vector - other)

    def __eq__(self, other: "Point") -> bool:
        """
        Check if two points are equal.

        Args:
          other (Point): The point to compare this one to.
        """
        return np.array_equal(self.vector, other.vector)

    @property
    def x(self) -> Number:
        """
        Return the x value of the point.
        """
        return self.vector[0]

    @property
    def y(self) -> Number:
        """
        Return the y value of the point.
        """
        return self.vector[1]

    @property
    def z(self) -> Number:
        """
        Return the z value of the point.
        """
        return self.vector[2]

    def dimension(self) -> int:
        """
        Return the dimension of the point.
        """
        return self.vector.dimension()

    def __repr__(self) -> str:
        """
        Return a string representation of the point.
        """
        return f"Point({self.vector.tolist()})"

    def __str__(self) -> str:
        """
        Return a string representation of the point.
        """
        return f"Point({self.vector.tolist()})"
