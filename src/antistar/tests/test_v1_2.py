"""Test the public interfaces and command-line features added in version 1.2."""

__all__: list[str] = [
    "TestV12Executable",
    "TestV12Main",
    "TestV12ParseArgs",
    "TestV12PublicAPI",
    "TestV12Run",
]

import inspect
import runpy
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from typing import Self
from unittest.mock import MagicMock, patch

import antistar
import antistar.core


class TestV12PublicAPI(unittest.TestCase):
    """Test the v1.2 functions exposed by the top-level package."""

    def test_main_is_reexported(self: Self, /) -> None:
        self.assertIs(antistar.main, antistar.core.main)

    def test_parse_args_is_reexported(self: Self, /) -> None:
        self.assertIs(antistar.parse_args, antistar.core.parse_args)

    def test_run_is_reexported(self: Self, /) -> None:
        self.assertIs(antistar.run, antistar.core.run)

    def test_starred_argument_is_named_items(self: Self, /) -> None:
        parameters: tuple[inspect.Parameter, ...]
        parameters = tuple(
            inspect.signature(antistar.antistar).parameters.values()
        )
        self.assertEqual(len(parameters), 1)
        self.assertEqual(parameters[0].name, "items")
        self.assertEqual(parameters[0].kind, inspect.Parameter.VAR_POSITIONAL)


class TestV12ParseArgs(unittest.TestCase):
    """Test argument parsing, help, and version options."""

    def test_no_items(self: Self, /) -> None:
        self.assertEqual(antistar.parse_args([]).items, [])

    def test_one_item(self: Self, /) -> None:
        self.assertEqual(antistar.parse_args(["alpha"]).items, ["alpha"])

    def test_multiple_items_keep_their_order(self: Self, /) -> None:
        self.assertEqual(
            antistar.parse_args(["alpha", "42", "alpha"]).items,
            ["alpha", "42", "alpha"],
        )

    def test_accepts_an_iterable_instead_of_a_list(self: Self, /) -> None:
        self.assertEqual(
            antistar.parse_args(iter(("first", "second"))).items,
            ["first", "second"],
        )

    def test_double_dash_treats_options_as_items(self: Self, /) -> None:
        self.assertEqual(
            antistar.parse_args(["--", "--help", "-V"]).items,
            ["--help", "-V"],
        )

    def test_short_help(self: Self, /) -> None:
        caught: unittest.case._AssertRaisesContext[SystemExit]
        output: StringIO
        output = StringIO()
        with redirect_stdout(output), self.assertRaises(SystemExit) as caught:
            antistar.parse_args(["-h"])
        self.assertEqual(caught.exception.code, 0)
        self.assertIn("usage: antistar", output.getvalue())
        self.assertIn("items", output.getvalue())

    def test_long_help(self: Self, /) -> None:
        caught: unittest.case._AssertRaisesContext[SystemExit]
        output: StringIO
        output = StringIO()
        with redirect_stdout(output), self.assertRaises(SystemExit) as caught:
            antistar.parse_args(["--help"])
        self.assertEqual(caught.exception.code, 0)
        self.assertIn("--version", output.getvalue())
        self.assertIn("--help", output.getvalue())

    def test_short_version(self: Self, /) -> None:
        caught: unittest.case._AssertRaisesContext[SystemExit]
        output: StringIO
        output = StringIO()
        with patch(
            "antistar.core.metadata.version", return_value="1.2.0+local"
        ):
            with (
                redirect_stdout(output),
                self.assertRaises(SystemExit) as caught,
            ):
                antistar.parse_args(["-V"])
        self.assertEqual(caught.exception.code, 0)
        self.assertEqual(output.getvalue(), "antistar, version 1.2.0+local\n")

    def test_long_version(self: Self, /) -> None:
        caught: unittest.case._AssertRaisesContext[SystemExit]
        output: StringIO
        output = StringIO()
        with patch(
            "antistar.core.metadata.version", return_value="1.2.0+local"
        ):
            with (
                redirect_stdout(output),
                self.assertRaises(SystemExit) as caught,
            ):
                antistar.parse_args(["--version"])
        self.assertEqual(caught.exception.code, 0)
        self.assertEqual(output.getvalue(), "antistar, version 1.2.0+local\n")

    def test_unknown_option_exits_with_code_two(self: Self, /) -> None:
        caught: unittest.case._AssertRaisesContext[SystemExit]
        errors: StringIO
        errors = StringIO()
        with redirect_stderr(errors), self.assertRaises(SystemExit) as caught:
            antistar.parse_args(["--unknown"])
        self.assertEqual(caught.exception.code, 2)
        self.assertIn("unrecognized arguments", errors.getvalue())


class TestV12Run(unittest.TestCase):
    """Test the printing wrapper added in version 1.2."""

    def test_run_with_no_items_prints_empty_tuple(self: Self, /) -> None:
        output: StringIO
        output = StringIO()
        with redirect_stdout(output):
            self.assertIsNone(antistar.run())  # type: ignore[func-returns-value]
        self.assertEqual(output.getvalue(), "()\n")

    def test_run_with_one_item_prints_singleton_tuple(self: Self, /) -> None:
        output: StringIO
        output = StringIO()
        with redirect_stdout(output):
            antistar.run("one")
        self.assertEqual(output.getvalue(), "('one',)\n")

    def test_run_with_mixed_items_preserves_order(self: Self, /) -> None:
        output: StringIO
        output = StringIO()
        with redirect_stdout(output):
            antistar.run("one", 2, None, False)
        self.assertEqual(output.getvalue(), "('one', 2, None, False)\n")


class TestV12Executable(unittest.TestCase):
    """Test executing the package initializer as a script."""

    def test_script_entry_point(self: Self, /) -> None:
        caught: unittest.case._AssertRaisesContext[SystemExit]
        output: StringIO
        output = StringIO()
        with patch.object(sys, "argv", ["antistar", "alpha", "beta"]):
            with (
                redirect_stdout(output),
                self.assertRaises(SystemExit) as caught,
            ):
                runpy.run_path(antistar.__file__, run_name="__main__")
        self.assertEqual(caught.exception.code, 0)
        self.assertEqual(output.getvalue(), "('alpha', 'beta')\n")


class TestV12Main(unittest.TestCase):
    """Test CLI success, option handling, and error exit codes."""

    def test_success_with_no_items(self: Self, /) -> None:
        output: StringIO
        result: int
        output = StringIO()
        with redirect_stdout(output):
            result = antistar.main([])
        self.assertEqual(result, 0)
        self.assertEqual(output.getvalue(), "()\n")

    def test_success_with_multiple_items(self: Self, /) -> None:
        output: StringIO
        result: int
        output = StringIO()
        with redirect_stdout(output):
            result = antistar.main(["one", "two"])
        self.assertEqual(result, 0)
        self.assertEqual(output.getvalue(), "('one', 'two')\n")

    def test_help_returns_zero(self: Self, /) -> None:
        output: StringIO
        result: int
        output = StringIO()
        with redirect_stdout(output):
            result = antistar.main(["--help"])
        self.assertEqual(result, 0)
        self.assertIn("usage: antistar", output.getvalue())

    def test_version_returns_zero(self: Self, /) -> None:
        output: StringIO
        result: int
        output = StringIO()
        with patch(
            "antistar.core.metadata.version", return_value="1.2.0+local"
        ):
            with redirect_stdout(output):
                result = antistar.main(["--version"])
        self.assertEqual(result, 0)
        self.assertEqual(output.getvalue(), "antistar, version 1.2.0+local\n")

    def test_parse_error_returns_two(self: Self, /) -> None:
        errors: StringIO
        result: int
        errors = StringIO()
        with redirect_stderr(errors):
            result = antistar.main(["--unknown"])
        self.assertEqual(result, 2)
        self.assertIn("unrecognized arguments", errors.getvalue())

    def test_integer_system_exit_code_is_preserved(self: Self, /) -> None:
        with patch("antistar.core.parse_args", side_effect=SystemExit(7)):
            self.assertEqual(antistar.main([]), 7)

    def test_noninteger_system_exit_code_is_failure(self: Self, /) -> None:
        with patch(
            "antistar.core.parse_args", side_effect=SystemExit("error")
        ):
            self.assertEqual(antistar.main([]), 1)

    def test_run_exception_is_logged_and_returns_one(self: Self, /) -> None:
        log_exception: MagicMock
        result: int
        with patch("antistar.core.run", side_effect=RuntimeError("failure")):
            with patch("antistar.core.logging.exception") as log_exception:
                result = antistar.main(["item"])
        self.assertEqual(result, 1)
        log_exception.assert_called_once()
        self.assertIsInstance(log_exception.call_args.args[0], RuntimeError)


if __name__ == "__main__":
    unittest.main()
