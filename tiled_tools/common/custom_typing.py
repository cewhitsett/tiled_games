"""
Custom typing defintions, useful as Number is a complex
type to work with.
"""

from numbers import Number
from typing import Any, Union

AnyNumber = Union[int, float, Number]


def is_numeric(value: Any) -> bool:
    """
    Check if a value is numeric.

    Args:
      value (AnyNumber): The value to check.

    Returns:
      bool: True if the value is numeric, False otherwise.
    """
    return isinstance(value, (int, float, Number))
