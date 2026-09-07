"""Regression tests for custom plot output paths."""

import os
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "01_Numerical_Methods"))
sys.path.insert(0, str(PROJECT_ROOT / "02_Computational_Physics"))
sys.path.insert(0, str(PROJECT_ROOT / "04_Robotics_Simulator"))

from automatic_water_tank import save_water_tank_plot, simulate_water_tank
from bouncing_ball import save_bounce_plot, simulate_bouncing_ball
from bridge_load_distribution import generate_load_study, save_load_plot
from center_of_mass import save_center_of_mass_plot
from random_walk_diffusion import save_diffusion_plot, simulate_random_walks
from two_link_arm_workspace import generate_workspace, save_workspace_plot


class PlotOutputPathTests(unittest.TestCase):
    def test_plot_functions_create_custom_output_directories(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)

            water_tank_path = root / "water_tank" / "plot.png"
            save_water_tank_plot(
                simulate_water_tank(duration_s=1.0),
                str(water_tank_path),
            )

            bouncing_ball_path = root / "bouncing_ball" / "plot.png"
            save_bounce_plot(
                simulate_bouncing_ball(maximum_time=0.01),
                str(bouncing_ball_path),
            )

            bridge_path = root / "bridge" / "plot.png"
            save_load_plot(
                generate_load_study(number_of_positions=3),
                str(bridge_path),
            )

            center_of_mass_path = root / "center_of_mass" / "plot.png"
            save_center_of_mass_plot(
                [1.0, 2.0],
                [0.0, 1.0],
                [0.0, 1.0],
                ["A", "B"],
                str(center_of_mass_path),
            )

            for output_path in (
                water_tank_path,
                bouncing_ball_path,
                bridge_path,
                center_of_mass_path,
            ):
                with self.subTest(output_path=output_path):
                    self.assertTrue(output_path.is_file())

    def test_plot_functions_accept_a_filename_without_a_directory(self):
        original_directory = Path.cwd()

        with tempfile.TemporaryDirectory() as temporary_directory:
            try:
                os.chdir(temporary_directory)

                save_diffusion_plot(
                    simulate_random_walks(2, 2),
                    "diffusion.png",
                )
                save_workspace_plot(
                    generate_workspace(angle_step_degrees=180),
                    "workspace.png",
                )

                self.assertTrue(Path("diffusion.png").is_file())
                self.assertTrue(Path("workspace.png").is_file())
            finally:
                os.chdir(original_directory)


if __name__ == "__main__":
    unittest.main()
