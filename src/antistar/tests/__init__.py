"""Provide the test runner for antistar."""

__all__: list[str] = ["test"]

import unittest


def test() -> unittest.TextTestResult:
    """Run all the tests."""
    loader: unittest.TestLoader
    runner: unittest.TextTestRunner
    suite: unittest.TestSuite
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="antistar.tests")
    runner = unittest.TextTestRunner()
    return runner.run(suite)
