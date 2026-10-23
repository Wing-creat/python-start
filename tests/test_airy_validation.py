"""Independent Airy benchmarks and checks on the comparison setup."""

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "05_Optics"))
from airy_validation import airy_intensity, compare_airy


class AiryValidationTests(unittest.TestCase):
    def test_center_and_first_dark_ring(self):
        # First positive zero of J1, tabulated independently of the FFT.
        first_zero = 3.8317059702
        values = airy_intensity([0, first_zero / (2 * np.pi * 0.35)], 0.35)
        self.assertEqual(values[0], 1)
        self.assertLess(values[1], 1e-20)

    def test_even_symmetry(self):
        np.testing.assert_allclose(airy_intensity([-2, -1], 0.35),
                                   airy_intensity([2, 1], 0.35))

    def test_shared_axis_and_refinement(self):
        coarse_f, coarse, theory = compare_airy(33)
        fine_f, fine, fine_theory = compare_airy(257)
        np.testing.assert_array_equal(coarse_f, fine_f)
        np.testing.assert_array_equal(theory, fine_theory)
        self.assertEqual(len(fine_f), 97)
        self.assertEqual(fine_f[0], -6)
        self.assertEqual(fine_f[-1], 6)
        self.assertAlmostEqual(fine[48], 1)
        self.assertLess(np.sqrt(np.mean((fine - theory) ** 2)), 0.001)
        self.assertLess(np.linalg.norm(fine - theory), np.linalg.norm(coarse - theory))

    def test_invalid_inputs(self):
        for radius in (0, -1, float("nan")):
            with self.assertRaises(ValueError):
                airy_intensity([0, 1], radius)
        with self.assertRaises(ValueError):
            airy_intensity([float("inf")], 0.35)
        for size, radius in ((9, 0.35), (32, 0.35), (33, 1.1)):
            with self.assertRaises(ValueError):
                compare_airy(size, aperture_radius=radius)


if __name__ == "__main__":
    unittest.main()
