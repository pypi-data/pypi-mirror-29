import unittest
from sgcalculator.src.exceptions import InvalidInputException

class TestExceptionMethods(unittest.TestCase):

    def test_NotNull(self):
        self.assertIsNotNone(InvalidInputException())
        

if __name__ == '__main__':
    unittest.main()
