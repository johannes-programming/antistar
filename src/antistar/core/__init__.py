from typing import TypeVar

__all__ = ["antistar"]

Arg = TypeVar("Arg")


def antistar(*args: Arg) -> tuple[Arg, ...]:
    "This function returns its positional arguments as a tuple."
    return args
