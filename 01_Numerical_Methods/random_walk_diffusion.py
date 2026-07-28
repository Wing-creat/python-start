"""Simulate two-dimensional random walks and compare diffusion with theory."""

import math
import os
import random

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUTPUT_PATH = "assets/random_walk_diffusion.png"


def simulate_random_walks(
    num_walkers: int,
    num_steps: int,
    step_length: float = 1.0,
    seed: int = 42,
) -> dict:
    """Return paths and mean-square displacement for 2D random walkers."""
    if num_walkers <= 0:
        raise ValueError("Number of walkers must be positive.")
    if num_steps <= 0:
        raise ValueError("Number of steps must be positive.")
    if step_length <= 0:
        raise ValueError("Step length must be positive.")

    random_generator = random.Random(seed)
    x_positions = [[0.0] for _ in range(num_walkers)]
    y_positions = [[0.0] for _ in range(num_walkers)]
    mean_square_displacement = [0.0]

    for _ in range(num_steps):
        squared_distances = []

        for walker_index in range(num_walkers):
            angle = random_generator.uniform(0.0, 2.0 * math.pi)
            new_x = x_positions[walker_index][-1] + step_length * math.cos(angle)
            new_y = y_positions[walker_index][-1] + step_length * math.sin(angle)

            x_positions[walker_index].append(new_x)
            y_positions[walker_index].append(new_y)
            squared_distances.append(new_x**2 + new_y**2)

        average_squared_distance = sum(squared_distances) / num_walkers
        mean_square_displacement.append(average_squared_distance)

    steps = list(range(num_steps + 1))
    theoretical_msd = [step * step_length**2 for step in steps]

    return {
        "steps": steps,
        "x_positions": x_positions,
        "y_positions": y_positions,
        "mean_square_displacement": mean_square_displacement,
        "theoretical_msd": theoretical_msd,
        "step_length": step_length,
        "seed": seed,
    }


def save_diffusion_plot(results: dict, output_path: str = OUTPUT_PATH) -> None:
    """Save particle paths and mean-square displacement in one figure."""
    figure, axes = plt.subplots(1, 2, figsize=(13, 5.5))

    sample_count = min(12, len(results["x_positions"]))
    for walker_index in range(sample_count):
        axes[0].plot(
            results["x_positions"][walker_index],
            results["y_positions"][walker_index],
            linewidth=1.1,
            alpha=0.75,
        )

    final_x_positions = [positions[-1] for positions in results["x_positions"]]
    final_y_positions = [positions[-1] for positions in results["y_positions"]]
    axes[0].scatter(
        final_x_positions,
        final_y_positions,
        color="#111827",
        s=10,
        alpha=0.25,
        label="Final positions",
    )
    axes[0].scatter(0.0, 0.0, color="#dc2626", s=45, label="Start")
    axes[0].set_title(f"Sample Paths ({sample_count} shown)")
    axes[0].set_xlabel("x position")
    axes[0].set_ylabel("y position")
    axes[0].set_aspect("equal", adjustable="box")
    axes[0].grid(True, linestyle="--", alpha=0.4)
    axes[0].legend()

    axes[1].plot(
        results["steps"],
        results["mean_square_displacement"],
        color="#2563eb",
        linewidth=2.2,
        label="Simulation",
    )
    axes[1].plot(
        results["steps"],
        results["theoretical_msd"],
        color="#dc2626",
        linestyle="--",
        linewidth=2.2,
        label="Theory: MSD = N * step_length^2",
    )
    axes[1].set_title("Mean-Square Displacement")
    axes[1].set_xlabel("Number of steps")
    axes[1].set_ylabel("Mean-square displacement")
    axes[1].grid(True, linestyle="--", alpha=0.4)
    axes[1].legend()

    figure.suptitle("Two-Dimensional Random Walk Diffusion", fontsize=15)
    figure.tight_layout(rect=(0, 0, 1, 0.95))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    figure.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    simulation = simulate_random_walks(
        num_walkers=600,
        num_steps=300,
        step_length=0.5,
        seed=42,
    )
    save_diffusion_plot(simulation)

    simulated_final_msd = simulation["mean_square_displacement"][-1]
    theoretical_final_msd = simulation["theoretical_msd"][-1]
    relative_error = (
        abs(simulated_final_msd - theoretical_final_msd)
        / theoretical_final_msd
        * 100
    )

    print("--- Two-Dimensional Random Walk Diffusion ---")
    print("Walkers              : 600")
    print("Steps per walker     : 300")
    print("Step length          : 0.50")
    print(f"Simulated final MSD  : {simulated_final_msd:.2f}")
    print(f"Theoretical final MSD: {theoretical_final_msd:.2f}")
    print(f"Relative error       : {relative_error:.2f}%")
    print(f"Plot saved to {OUTPUT_PATH}")
