"""Run the tests for antistar."""

__all__: list[str] = ["main"]

import sys

import antistar.tests


def main() -> int:
    return int(not antistar.tests.test())


if __name__ == "__main__":
    sys.exit(main())
