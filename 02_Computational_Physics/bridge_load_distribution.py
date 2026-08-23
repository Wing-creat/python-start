"""Show how a moving load is shared by two bridge supports."""

import os

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUTPUT_PATH = "assets/bridge_load_distribution.png"


def calculate_support_forces(
    load_newtons: float,
    load_position_m: float,
    bridge_length_m: float,
) -> tuple:
    """Return the vertical forces at the left and right supports."""
    if load_newtons < 0:
        raise ValueError("Load cannot be negative.")
    if bridge_length_m <= 0:
        raise ValueError("Bridge length must be positive.")
    if not 0 <= load_position_m <= bridge_length_m:
        raise ValueError("Load position must be on the bridge.")

    right_support_force = load_newtons * load_position_m / bridge_length_m
    left_support_force = load_newtons - right_support_force

    return left_support_force, right_support_force


def generate_load_study(
    load_newtons: float = 1000.0,
    bridge_length_m: float = 6.0,
    number_of_positions: int = 121,
) -> dict:
    """Calculate support forces as one load moves across the bridge."""
    if number_of_positions < 2:
        raise ValueError("At least two load positions are required.")

    positions = [
        bridge_length_m * index / (number_of_positions - 1)
        for index in range(number_of_positions)
    ]
    left_forces = []
    right_forces = []

    for position in positions:
        left_force, right_force = calculate_support_forces(
            load_newtons,
            position,
            bridge_length_m,
        )
        left_forces.append(left_force)
        right_forces.append(right_force)

    return {
        "positions": positions,
        "left_forces": left_forces,
        "right_forces": right_forces,
        "load_newtons": load_newtons,
        "bridge_length_m": bridge_length_m,
    }


def save_load_plot(study: dict, output_path: str = OUTPUT_PATH) -> None:
    """Save a graph of the two support forces."""
    midpoint = study["bridge_length_m"] / 2

    plt.figure(figsize=(10, 6))
    plt.plot(
        study["positions"],
        study["left_forces"],
        color="#2563eb",
        linewidth=2.5,
        label="Left support",
    )
    plt.plot(
        study["positions"],
        study["right_forces"],
        color="#ea580c",
        linewidth=2.5,
        label="Right support",
    )
    plt.axvline(
        midpoint,
        color="#6b7280",
        linestyle="--",
        linewidth=1.5,
        label="Bridge midpoint",
    )

    plt.title("Bridge Support Forces for a Moving Load")
    plt.xlabel("Load Position from Left Support (m)")
    plt.ylabel("Support Force (N)")
    plt.xlim(0, study["bridge_length_m"])
    plt.ylim(bottom=0)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()

    os.makedirs("assets", exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    bridge_study = generate_load_study(
        load_newtons=1000.0,
        bridge_length_m=6.0,
    )
    save_load_plot(bridge_study)

    print("--- Bridge Load Distribution ---")
    print("Bridge length: 6.00 m")
    print("Moving load  : 1000 N\n")
    print(f"{'Position':>10} | {'Left Support':>12} | {'Right Support':>13}")
    print("-" * 43)

    for position in (0.0, 1.5, 3.0, 4.5, 6.0):
        left_force, right_force = calculate_support_forces(
            1000.0,
            position,
            6.0,
        )
        print(
            f"{position:>8.1f} m | "
            f"{left_force:>9.1f} N | "
            f"{right_force:>10.1f} N"
        )

    print("\nThe two support forces always add up to the moving load.")
    print(f"Plot saved to {OUTPUT_PATH}")
