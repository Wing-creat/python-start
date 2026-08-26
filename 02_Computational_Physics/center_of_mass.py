"""Calculate and visualize the center of mass of several point masses."""

import os

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUTPUT_PATH = "assets/center_of_mass.png"


def calculate_center_of_mass(
    masses: list,
    x_positions: list,
    y_positions: list,
) -> tuple:
    """Return total mass and the x and y coordinates of the center of mass."""
    if not masses:
        raise ValueError("At least one mass is required.")
    if not (len(masses) == len(x_positions) == len(y_positions)):
        raise ValueError("Mass and position lists must have matching lengths.")
    if any(mass <= 0 for mass in masses):
        raise ValueError("Every mass must be positive.")

    total_mass = sum(masses)
    weighted_x_sum = sum(
        mass * x_position
        for mass, x_position in zip(masses, x_positions)
    )
    weighted_y_sum = sum(
        mass * y_position
        for mass, y_position in zip(masses, y_positions)
    )

    center_x = weighted_x_sum / total_mass
    center_y = weighted_y_sum / total_mass

    return total_mass, center_x, center_y


def save_center_of_mass_plot(
    masses: list,
    x_positions: list,
    y_positions: list,
    labels: list,
    output_path: str = OUTPUT_PATH,
) -> None:
    """Save a graph of the point masses and their center of mass."""
    total_mass, center_x, center_y = calculate_center_of_mass(
        masses,
        x_positions,
        y_positions,
    )
    if len(labels) != len(masses):
        raise ValueError("Each mass must have one label.")

    marker_sizes = [mass * 180 for mass in masses]

    plt.figure(figsize=(8, 7))
    plt.scatter(
        x_positions,
        y_positions,
        s=marker_sizes,
        color="#2563eb",
        alpha=0.75,
        edgecolors="black",
        label="Point masses",
    )

    for label, mass, x_position, y_position in zip(
        labels,
        masses,
        x_positions,
        y_positions,
    ):
        plt.annotate(
            f"{label}: {mass:g} kg",
            (x_position, y_position),
            xytext=(8, 8),
            textcoords="offset points",
        )

    plt.scatter(
        center_x,
        center_y,
        s=300,
        marker="*",
        color="#dc2626",
        edgecolors="black",
        label=f"Center of mass ({center_x:.2f}, {center_y:.2f}) m",
        zorder=3,
    )
    plt.axhline(0, color="#6b7280", linewidth=1)
    plt.axvline(0, color="#6b7280", linewidth=1)
    plt.title(
        f"Center of Mass of {len(masses)} Point Masses "
        f"(Total: {total_mass:g} kg)"
    )
    plt.xlabel("x Position (m)")
    plt.ylabel("y Position (m)")
    plt.axis("equal")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend(loc="lower right")

    os.makedirs("assets", exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    example_labels = ["A", "B", "C", "D"]
    example_masses = [2.0, 1.0, 3.0, 4.0]
    example_x_positions = [-2.0, 2.0, 0.0, 0.0]
    example_y_positions = [0.0, 0.0, 2.0, -1.0]

    total, center_x, center_y = calculate_center_of_mass(
        example_masses,
        example_x_positions,
        example_y_positions,
    )
    save_center_of_mass_plot(
        example_masses,
        example_x_positions,
        example_y_positions,
        example_labels,
    )

    print("--- Center of Mass ---")
    print(f"{'Mass':>6} | {'Value':>9} | {'x':>7} | {'y':>7}")
    print("-" * 39)
    for label, mass, x_position, y_position in zip(
        example_labels,
        example_masses,
        example_x_positions,
        example_y_positions,
    ):
        print(
            f"{label:>6} | {mass:>6.1f} kg | "
            f"{x_position:>5.1f} m | {y_position:>5.1f} m"
        )

    print(f"\nTotal mass: {total:.1f} kg")
    print(f"Center of mass: ({center_x:.2f} m, {center_y:.2f} m)")
    print(f"Plot saved to {OUTPUT_PATH}")
