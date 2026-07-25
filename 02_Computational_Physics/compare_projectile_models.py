"""Compare ideal projectile motion with a quadratic air-drag model."""

import os

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from projectile_drag import simulate_drag_trajectory
from projectile_sim import simulate_vacuum_trajectory


INITIAL_SPEED = 50.0
LAUNCH_ANGLE = 45.0
PROJECTILE_MASS = 0.145
DRAG_COEFFICIENT = 0.47
CROSS_SECTIONAL_AREA = 0.0042
AIR_DENSITY = 1.225
TIME_STEP = 0.01
OUTPUT_PATH = "assets/projectile_drag_comparison.png"


def print_result_table(vacuum_trajectory: dict, drag_trajectory: dict) -> None:
    """Print the main results from both trajectory models."""
    print("\nProjectile Model Comparison")
    print("-" * 62)
    print(f"{'Model':<20}{'Flight Time (s)':>15}{'Max Height (m)':>15}{'Range (m)':>12}")
    print("-" * 62)

    for model_name, trajectory in (
        ("Vacuum", vacuum_trajectory),
        ("Quadratic drag", drag_trajectory),
    ):
        print(
            f"{model_name:<20}"
            f"{trajectory['flight_time']:>15.2f}"
            f"{trajectory['max_height']:>15.2f}"
            f"{trajectory['range']:>12.2f}"
        )

    print("-" * 62)


def compare_projectile_models() -> tuple:
    """Run both models, save a comparison plot, and return their results."""
    vacuum_trajectory = simulate_vacuum_trajectory(
        INITIAL_SPEED,
        LAUNCH_ANGLE,
    )
    drag_trajectory = simulate_drag_trajectory(
        v0=INITIAL_SPEED,
        angle_degrees=LAUNCH_ANGLE,
        mass_kg=PROJECTILE_MASS,
        drag_coefficient=DRAG_COEFFICIENT,
        area_m2=CROSS_SECTIONAL_AREA,
        air_density=AIR_DENSITY,
        time_step=TIME_STEP,
    )

    print(f"Initial speed: {INITIAL_SPEED:.1f} m/s")
    print(f"Launch angle: {LAUNCH_ANGLE:.1f} degrees")
    print(f"Projectile mass: {PROJECTILE_MASS:.3f} kg")
    print_result_table(vacuum_trajectory, drag_trajectory)

    plt.figure(figsize=(10, 6))
    plt.plot(
        vacuum_trajectory["x_positions"],
        vacuum_trajectory["y_positions"],
        label="Vacuum (analytical)",
        color="#2563eb",
        linewidth=2.5,
    )
    plt.plot(
        drag_trajectory["x_positions"],
        drag_trajectory["y_positions"],
        label="Quadratic drag (RK4)",
        color="#dc2626",
        linewidth=2.5,
    )

    plt.title("Projectile Motion: Vacuum vs Quadratic Air Drag")
    plt.xlabel("Horizontal Distance (m)")
    plt.ylabel("Vertical Height (m)")
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()

    os.makedirs("assets", exist_ok=True)
    plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\nComparison plot saved to {OUTPUT_PATH}")
    return vacuum_trajectory, drag_trajectory


if __name__ == "__main__":
    compare_projectile_models()
