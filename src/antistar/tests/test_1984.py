"""Provide unit tests for the antistar package."""

__all__ = ["TestAntistar"]

import unittest
from typing import Any, Self

import antistar


class TestAntistar(unittest.TestCase):
    """Test the antistar function."""

    def test_empty_args(self: Self) -> None:
        """Test the antistar function with no arguments."""
        result: tuple[Any, ...]
        result = antistar.antistar()
        self.assertEqual(result, ())

    def test_single_arg(self: Self) -> None:
        """Test the antistar function with a single argument."""
        result: tuple[Any, ...]
        result = antistar.antistar(42)
        self.assertEqual(result, (42,))

    def test_multiple_args(self: Self) -> None:
        """Test the antistar function with multiple heterogeneous arguments."""
        result: tuple[Any, ...]
        result = antistar.antistar("hello", 3.14, True, None)
        self.assertEqual(result, ("hello", 3.14, True, None))

    def test_order_preservation(self: Self) -> None:
        """Test that the order of arguments is preserved."""
        result: tuple[Any, ...]
        result = antistar.antistar(1, 2, 3)
        self.assertEqual(result, (1, 2, 3))


if __name__ == "__main__":
    unittest.main()
