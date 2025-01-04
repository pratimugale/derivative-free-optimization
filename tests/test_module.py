import unittest
from optimizers.module import Optimizer

class GreetTestCase(unittest.TestCase):
    def test_greet(self):
        opt = Optimizer()
        self.assertEqual(opt.greet("Alice"), "Hello, Alice! Welcome to my library.")
        self.assertEqual(opt.greet("Bob"), "Hello, Bob! Welcome to my library.")

if __name__ == "__main__":
    unittest.main()