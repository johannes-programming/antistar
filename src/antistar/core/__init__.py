"""Provide the core antistar functionality."""

__all__: list[str] = ["antistar"]

from typing import TypeVar

Arg = TypeVar("Arg")


def antistar(*args: Arg) -> tuple[Arg, ...]:
    """Return the positional arguments as a tuple."""
    return args
