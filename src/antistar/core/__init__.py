"""Provide the core antistar functionality."""

__all__: list[str] = ["antistar", "main", "parse_args", "run"]

import argparse
import logging
from collections import abc
from importlib import metadata
from typing import TypeVar

Item = TypeVar("Item")


def antistar(*items: Item) -> tuple[Item, ...]:
    """Return the positional arguments as a tuple."""
    return items


def main(args: abc.Iterable[str] | None = None) -> int:
    space: argparse.Namespace
    try:
        space = parse_args(args)
        run(*space.items)
    except SystemExit as exit:
        if isinstance(exit.code, int):
            return int(exit.code)
        else:
            return int(bool(exit.code))
    except BaseException as exc:
        logging.exception(exc)
        return 1
    else:
        return 0


def parse_args(args: abc.Iterable[str] | None = None) -> argparse.Namespace:
    parser: argparse.ArgumentParser
    version: str
    parser = argparse.ArgumentParser(
        add_help=False,
        description="Convert positional arguments to tuple.",
        prog="antistar",
    )
    version = "%(prog)s, version " + metadata.version("antistar")
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        help="print the version and abort",
        version=version,
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="print this message and abort",
    )
    parser.add_argument(
        "items",
        help="items for the tuple",
        nargs="*",
    )
    return parser.parse_args(args)


def run(*items: object) -> None:
    print(antistar(*items))
