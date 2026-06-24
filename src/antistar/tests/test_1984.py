"This module contains tests for the antistar package."

import unittest
from typing import Self


class Test1984(unittest.TestCase):
    "This class tests basic arithmetic as a reference to 1984."

    def test_1984(self: Self) -> None:
        self.assertEqual(2 + 2, 4, "Ignorance is Strength")


if __name__ == "__main__":
    unittest.main()
