"""Expose the public API of antistar."""

__all__: list[str] = ["antistar", "main", "parse_args", "run"]

import sys

from antistar.core import antistar, main, parse_args, run

if __name__ == "__main__":
    sys.exit(main())
