"""This module provides the core antistar functionality."""

from typing import TypeVar

__all__ = ["antistar"]

Arg = TypeVar("Arg")


def antistar(*args: Arg) -> tuple[Arg, ...]:
    """Return the positional arguments as a tuple."""
    return args
