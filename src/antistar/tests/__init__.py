"""Provide the test runner for antistar."""

__all__: list[str] = ["test"]

import unittest


def test() -> unittest.TextTestResult:
    """Run all the tests."""
    loader: unittest.TestLoader
    suite: unittest.TestSuite
    runner: unittest.TextTestRunner
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="antistar.tests")
    runner = unittest.TextTestRunner()
    return runner.run(suite)
