import unittest

__all__ = ["test"]


def test() -> unittest.TextTestResult:
    "This function runs all the tests."
    loader: unittest.TestLoader
    suite: unittest.TestSuite
    runner: unittest.TextTestRunner
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="antistar.tests")
    runner = unittest.TextTestRunner()
    return runner.run(suite)
