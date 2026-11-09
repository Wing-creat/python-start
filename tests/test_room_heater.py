"""Tests for the ideal room-heater energy model."""

import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PHYSICS_DIRECTORY = PROJECT_ROOT / "02_Computational_Physics"
sys.path.insert(0, str(PHYSICS_DIRECTORY))

from room_heater import (
    calculate_air_mass,
    calculate_heater_resistance,
    calculate_heating_energy,
    calculate_heating_time_minutes,
    calculate_ideal_temperature,
    save_heating_plot,
)


class RoomHeaterTests(unittest.TestCase):
    def test_example_room_contains_120_kg_of_air(self):
        air_mass_kg = calculate_air_mass(
            floor_area_m2=25.0,
            room_height_m=4.0,
            air_density_kg_m3=1.2,
        )

        self.assertAlmostEqual(air_mass_kg, 120.0)

    def test_example_temperature_change_needs_844200_joules(self):
        energy_j = calculate_heating_energy(
            air_mass_kg=120.0,
            specific_heat_j_kg_c=1005.0,
            initial_temperature_c=15.0,
            target_temperature_c=22.0,
        )

        self.assertAlmostEqual(energy_j, 844200.0)

    def test_half_setting_doubles_the_ideal_heating_time(self):
        full_power_time = calculate_heating_time_minutes(
            energy_j=844200.0,
            rated_power_w=1500.0,
            heater_setting=1.0,
        )
        half_power_time = calculate_heating_time_minutes(
            energy_j=844200.0,
            rated_power_w=1500.0,
            heater_setting=0.5,
        )

        self.assertAlmostEqual(full_power_time, 9.38)
        self.assertAlmostEqual(half_power_time, 2 * full_power_time)

    def test_1500_watt_heater_has_9_point_6_ohm_resistance(self):
        resistance_ohm = calculate_heater_resistance(
            voltage_v=120.0,
            rated_power_w=1500.0,
        )

        self.assertAlmostEqual(resistance_ohm, 9.6)

    def test_full_power_temperature_reaches_target_at_calculated_time(self):
        heating_time_min = calculate_heating_time_minutes(
            energy_j=844200.0,
            rated_power_w=1500.0,
            heater_setting=1.0,
        )

        temperature_c = calculate_ideal_temperature(
            time_min=heating_time_min,
            initial_temperature_c=15.0,
            air_mass_kg=120.0,
            specific_heat_j_kg_c=1005.0,
            rated_power_w=1500.0,
            heater_setting=1.0,
        )

        self.assertAlmostEqual(temperature_c, 22.0)

    def test_doubled_floor_area_doubles_mass_and_heating_time(self):
        small_mass = calculate_air_mass(25.0, 4.0)
        large_mass = calculate_air_mass(50.0, 4.0)
        small_energy = calculate_heating_energy(
            small_mass,
            1005.0,
            15.0,
            22.0,
        )
        large_energy = calculate_heating_energy(
            large_mass,
            1005.0,
            15.0,
            22.0,
        )
        small_time = calculate_heating_time_minutes(small_energy, 1500.0)
        large_time = calculate_heating_time_minutes(large_energy, 1500.0)

        self.assertAlmostEqual(large_mass, 2 * small_mass)
        self.assertAlmostEqual(large_time, 2 * small_time)

    def test_invalid_air_mass_inputs_are_rejected(self):
        for values in (
            (0.0, 4.0, 1.2),
            (25.0, -1.0, 1.2),
            (25.0, 4.0, 0.0),
            (float("nan"), 4.0, 1.2),
        ):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    calculate_air_mass(*values)

    def test_invalid_energy_and_power_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            calculate_heating_energy(0.0, 1005.0, 15.0, 22.0)
        with self.assertRaises(ValueError):
            calculate_heating_energy(120.0, 0.0, 15.0, 22.0)
        with self.assertRaises(ValueError):
            calculate_heating_energy(120.0, 1005.0, 22.0, 15.0)
        with self.assertRaises(ValueError):
            calculate_heating_time_minutes(0.0, 1500.0)
        with self.assertRaises(ValueError):
            calculate_heating_time_minutes(844200.0, 0.0)

    def test_invalid_settings_and_time_are_rejected(self):
        for heater_setting in (0.0, -0.1, 1.1, float("nan")):
            with self.subTest(heater_setting=heater_setting):
                with self.assertRaises(ValueError):
                    calculate_heating_time_minutes(
                        844200.0,
                        1500.0,
                        heater_setting,
                    )
        with self.assertRaises(ValueError):
            calculate_ideal_temperature(
                -1.0,
                15.0,
                120.0,
                1005.0,
                1500.0,
            )

    def test_invalid_resistance_inputs_are_rejected(self):
        for voltage_v, rated_power_w in (
            (0.0, 1500.0),
            (120.0, 0.0),
            (float("inf"), 1500.0),
        ):
            with self.subTest(voltage_v=voltage_v, rated_power_w=rated_power_w):
                with self.assertRaises(ValueError):
                    calculate_heater_resistance(voltage_v, rated_power_w)

    def test_plot_creates_a_custom_output_directory(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = (
                Path(temporary_directory)
                / "heating"
                / "room.png"
            )
            save_heating_plot(
                times_min=[0.0, 1.0, 2.0],
                temperatures_by_setting={
                    0.5: [15.0, 15.5, 16.0],
                    1.0: [15.0, 16.0, 17.0],
                },
                target_temperature_c=22.0,
                output_path=str(output_path),
            )

            self.assertTrue(output_path.is_file())


if __name__ == "__main__":
    unittest.main()
