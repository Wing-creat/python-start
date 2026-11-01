"""Correct a horizontal beam offset with simple proportional feedback."""

import math
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import numpy as np

from beam_alignment import simulate_beam_positions
from beam_noise_study import simulate_noisy_measurements


OUTPUT_PATH = "assets/beam_feedback_control.png"


def simulate_alignment_control(
    initial_tilt_waves: float,
    controller_gain: float,
    noise_standard_deviation: float,
    number_of_steps: int = 15,
    random_seed: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return tilt, true-position, and measured-position control histories."""
    if not math.isfinite(initial_tilt_waves):
        raise ValueError("Initial tilt must be finite.")
    if not math.isfinite(controller_gain) or controller_gain <= 0:
        raise ValueError("Controller gain must be finite and positive.")
    if isinstance(number_of_steps, bool) or not isinstance(number_of_steps, int):
        raise ValueError("Number of steps must be an integer.")
    if number_of_steps < 2:
        raise ValueError("Number of steps must be at least 2.")

    measurement_noise = simulate_noisy_measurements(
        true_position=0.0,
        noise_standard_deviation=noise_standard_deviation,
        number_of_measurements=number_of_steps,
        random_seed=random_seed,
    )
    tilt_history = []
    true_positions = []
    measured_positions = []
    current_tilt = float(initial_tilt_waves)

    for step_index in range(number_of_steps):
        true_position = float(
            simulate_beam_positions(np.array([current_tilt]))[0]
        )
        measured_position = true_position + measurement_noise[step_index]

        tilt_history.append(current_tilt)
        true_positions.append(true_position)
        measured_positions.append(measured_position)

        if step_index < number_of_steps - 1:
            current_tilt -= controller_gain * measured_position

    return (
        np.asarray(tilt_history),
        np.asarray(true_positions),
        np.asarray(measured_positions),
    )


def save_control_history_plot(
    tilt_history: np.ndarray,
    true_positions: np.ndarray,
    measured_positions: np.ndarray,
    output_path: str = OUTPUT_PATH,
) -> None:
    """Save beam-position and wavefront-tilt histories for one control run."""
    correction_steps = np.arange(len(tilt_history))
    figure, axes = plt.subplots(
        2,
        1,
        figsize=(8, 7),
        sharex=True,
        layout="constrained",
    )

    axes[0].plot(
        correction_steps,
        true_positions,
        "o-",
        color="#2563eb",
        label="True beam position",
    )
    axes[0].scatter(
        correction_steps,
        measured_positions,
        color="#f59e0b",
        marker="x",
        s=45,
        label="Noisy measurement",
    )
    axes[0].axhline(0.0, color="black", linewidth=0.8, linestyle="--")
    axes[0].set_ylabel("Beam position (detector pixels)")
    axes[0].set_title("Proportional Beam Alignment with Measurement Noise")
    axes[0].grid(alpha=0.3)
    axes[0].legend()

    axes[1].plot(
        correction_steps,
        tilt_history,
        "o-",
        color="#7c3aed",
    )
    axes[1].axhline(0.0, color="black", linewidth=0.8, linestyle="--")
    axes[1].set_xlabel("Correction step")
    axes[1].set_ylabel("Wavefront tilt (waves)")
    axes[1].grid(alpha=0.3)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main() -> None:
    """Run the Day Three proportional-feedback example."""
    initial_tilt_waves = 1.5
    controller_gain = 0.20
    noise_standard_deviation = 0.05
    number_of_steps = 15
    random_seed = 42

    tilt_history, true_positions, measured_positions = (
        simulate_alignment_control(
            initial_tilt_waves=initial_tilt_waves,
            controller_gain=controller_gain,
            noise_standard_deviation=noise_standard_deviation,
            number_of_steps=number_of_steps,
            random_seed=random_seed,
        )
    )
    save_control_history_plot(
        tilt_history,
        true_positions,
        measured_positions,
    )

    absolute_reduction = abs(true_positions[0]) - abs(true_positions[-1])
    print("--- Active Optical Alignment: Day Three ---")
    print(f"Initial tilt: {initial_tilt_waves:.2f} waves")
    print(
        "Controller gain: "
        f"{controller_gain:.2f} waves per detector pixel"
    )
    print(
        "Measurement noise sigma: "
        f"{noise_standard_deviation:.2f} detector pixel"
    )
    print(f"Recorded correction steps: {number_of_steps}")
    print(f"Initial true position: {true_positions[0]:.4f} detector pixels")
    print(f"Final true position: {true_positions[-1]:.4f} detector pixels")
    print(f"Absolute position reduction: {absolute_reduction:.4f} detector pixels")
    print("Gain and noise comparisons: reserved for Day Four")
    print(f"Plot saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
