import unittest
from calculator import calculate_total

class CalculatorTests(unittest.TestCase):
    def test_ten_percent_discount(self):
        self.assertAlmostEqual(calculate_total(200, 10), 180.0)
    def test_no_discount(self):
        self.assertAlmostEqual(calculate_total(200, 0), 200.0)
    def test_full_discount(self):
        self.assertAlmostEqual(calculate_total(200, 100), 0.0)
    def test_invalid_discount(self):
        with self.assertRaises(ValueError):
            calculate_total(200, 101)

if __name__ == "__main__":
    unittest.main()
