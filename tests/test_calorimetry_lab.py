"""Tests for the simple calorimetry energy-balance model."""

import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PHYSICS_DIRECTORY = PROJECT_ROOT / "02_Computational_Physics"
sys.path.insert(0, str(PHYSICS_DIRECTORY))

from calorimetry_lab import (
    calculate_equilibrium_temperature,
    calculate_heat_transfer,
    save_calorimetry_plot,
)


class CalorimetryLabTests(unittest.TestCase):
    def test_aluminum_example_reaches_expected_temperature(self):
        final_temperature_c = calculate_equilibrium_temperature(
            metal_mass_g=100.0,
            metal_specific_heat_j_g_c=0.897,
            metal_initial_temperature_c=100.0,
            water_mass_g=100.0,
            water_initial_temperature_c=20.0,
        )

        self.assertAlmostEqual(final_temperature_c, 34.12, places=2)

    def test_equal_initial_temperatures_do_not_change(self):
        final_temperature_c = calculate_equilibrium_temperature(
            100.0,
            0.897,
            25.0,
            100.0,
            25.0,
        )

        self.assertAlmostEqual(final_temperature_c, 25.0)

    def test_equilibrium_stays_between_initial_temperatures(self):
        final_temperature_c = calculate_equilibrium_temperature(
            100.0,
            0.449,
            100.0,
            100.0,
            20.0,
        )

        self.assertGreater(final_temperature_c, 20.0)
        self.assertLess(final_temperature_c, 100.0)

    def test_signed_heat_transfers_balance(self):
        final_temperature_c = calculate_equilibrium_temperature(
            100.0,
            0.897,
            100.0,
            100.0,
            20.0,
        )
        metal_heat_j = calculate_heat_transfer(
            100.0,
            0.897,
            100.0,
            final_temperature_c,
        )
        water_heat_j = calculate_heat_transfer(
            100.0,
            4.184,
            20.0,
            final_temperature_c,
        )

        self.assertLess(metal_heat_j, 0.0)
        self.assertGreater(water_heat_j, 0.0)
        self.assertAlmostEqual(metal_heat_j + water_heat_j, 0.0)

    def test_aluminum_heats_water_more_than_iron_and_copper(self):
        temperatures_c = {
            material: calculate_equilibrium_temperature(
                100.0,
                specific_heat,
                100.0,
                100.0,
                20.0,
            )
            for material, specific_heat in {
                "Aluminum": 0.897,
                "Iron": 0.449,
                "Copper": 0.385,
            }.items()
        }

        self.assertGreater(temperatures_c["Aluminum"], temperatures_c["Iron"])
        self.assertGreater(temperatures_c["Iron"], temperatures_c["Copper"])

    def test_more_hot_metal_raises_equilibrium_temperature(self):
        light_sample_temperature_c = calculate_equilibrium_temperature(
            50.0,
            0.385,
            100.0,
            100.0,
            20.0,
        )
        heavy_sample_temperature_c = calculate_equilibrium_temperature(
            200.0,
            0.385,
            100.0,
            100.0,
            20.0,
        )

        self.assertGreater(
            heavy_sample_temperature_c,
            light_sample_temperature_c,
        )

    def test_invalid_masses_and_specific_heats_are_rejected(self):
        invalid_equilibrium_inputs = (
            (0.0, 0.897, 100.0, 100.0, 20.0, 4.184),
            (100.0, -0.897, 100.0, 100.0, 20.0, 4.184),
            (100.0, 0.897, 100.0, float("nan"), 20.0, 4.184),
            (100.0, 0.897, 100.0, 100.0, 20.0, float("inf")),
        )

        for values in invalid_equilibrium_inputs:
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    calculate_equilibrium_temperature(*values)

        with self.assertRaises(ValueError):
            calculate_heat_transfer(0.0, 0.897, 100.0, 30.0)
        with self.assertRaises(ValueError):
            calculate_heat_transfer(100.0, float("nan"), 100.0, 30.0)

    def test_non_finite_temperatures_are_rejected(self):
        with self.assertRaises(ValueError):
            calculate_equilibrium_temperature(
                100.0,
                0.897,
                float("inf"),
                100.0,
                20.0,
            )
        with self.assertRaises(ValueError):
            calculate_heat_transfer(
                100.0,
                0.897,
                100.0,
                float("nan"),
            )

    def test_plot_creates_a_custom_output_directory(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = (
                Path(temporary_directory)
                / "calorimetry"
                / "comparison.png"
            )
            save_calorimetry_plot(
                metal_masses_g=[50.0, 100.0, 150.0],
                temperatures_by_material={
                    "Aluminum": [28.0, 34.0, 39.0],
                    "Copper": [24.0, 27.0, 30.0],
                },
                output_path=str(output_path),
            )

            self.assertTrue(output_path.is_file())


if __name__ == "__main__":
    unittest.main()
