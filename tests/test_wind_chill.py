"""Check reference values, physical trends, and wind chill input limits."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "02_Computational_Physics"))

from wind_chill import calculate_wind_chill


class WindChillTests(unittest.TestCase):
    def test_reference_value(self):
        # The NWS chart gives about 21 F for 30 F air and 10 mph wind.
        result_c = calculate_wind_chill((30 - 32) * 5 / 9, 10 * 1.609344)
        self.assertAlmostEqual(result_c * 9 / 5 + 32, 21, delta=0.5)

    def test_stronger_wind_feels_colder(self):
        self.assertLess(calculate_wind_chill(5, 20), calculate_wind_chill(5, 5))
        self.assertLess(calculate_wind_chill(5, 5), 5)

    def test_warmer_air_feels_warmer(self):
        self.assertGreater(calculate_wind_chill(5, 20), calculate_wind_chill(0, 20))

    def test_boundary_is_accepted(self):
        self.assertTrue(isinstance(calculate_wind_chill(10, 5), float))

    def test_invalid_inputs(self):
        for temperature, wind in ((11, 10), (5, 0), (5, -1), (5, 4.9),
                                  (float("nan"), 10), (5, float("inf"))):
            with self.subTest(temperature=temperature, wind=wind):
                with self.assertRaises(ValueError):
                    calculate_wind_chill(temperature, wind)


if __name__ == "__main__":
    unittest.main()
