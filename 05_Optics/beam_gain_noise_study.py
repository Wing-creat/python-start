"""Compare proportional-control gains under several noise levels."""

import math
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import numpy as np

from beam_feedback_control import simulate_alignment_control


OUTPUT_PATH = "assets/beam_gain_noise_study.png"
GAIN_VALUES = (0.05, 0.20, 0.50)
NOISE_LEVELS = (0.00, 0.05, 0.20)
INITIAL_TILT_WAVES = 1.5
NUMBER_OF_STEPS = 40
RANDOM_SEED = 42
STEADY_STATE_STEPS = 10
SETTLING_TOLERANCE = 0.10


def _validate_position_history(true_positions: np.ndarray) -> np.ndarray:
    """Return a finite, non-empty, one-dimensional position array."""
    position_array = np.asarray(true_positions, dtype=float)
    if position_array.ndim != 1 or position_array.size == 0:
        raise ValueError("True positions must be a non-empty 1D array.")
    if not np.all(np.isfinite(position_array)):
        raise ValueError("True positions must be finite.")
    return position_array


def calculate_steady_state_rms(
    true_positions: np.ndarray,
    steady_state_steps: int = 10,
) -> float:
    """Return RMS true-position error over the final requested steps."""
    position_array = _validate_position_history(true_positions)
    if isinstance(steady_state_steps, bool) or not isinstance(
        steady_state_steps,
        int,
    ):
        raise ValueError("Steady-state steps must be an integer.")
    if steady_state_steps <= 0 or steady_state_steps > position_array.size:
        raise ValueError("Steady-state steps must fit inside the position history.")

    steady_positions = position_array[-steady_state_steps:]
    return float(np.sqrt(np.mean(steady_positions**2)))


def find_settling_step(
    true_positions: np.ndarray,
    tolerance: float = 0.10,
) -> int | None:
    """Return the first step after which true position stays within tolerance."""
    position_array = _validate_position_history(true_positions)
    if not math.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("Settling tolerance must be finite and positive.")

    for step_index in range(position_array.size):
        if np.all(np.abs(position_array[step_index:]) <= tolerance):
            return step_index
    return None


def run_parameter_study(
    gain_values: tuple[float, ...],
    noise_levels: tuple[float, ...],
    initial_tilt_waves: float = 1.5,
    number_of_steps: int = 40,
    random_seed: int = 42,
    steady_state_steps: int = 10,
    settling_tolerance: float = 0.10,
) -> dict[tuple[float, float], tuple[float, int | None]]:
    """Return RMS error and settling step for each gain and noise pair."""
    results = {}

    for controller_gain in gain_values:
        for noise_standard_deviation in noise_levels:
            _, true_positions, _ = simulate_alignment_control(
                initial_tilt_waves=initial_tilt_waves,
                controller_gain=controller_gain,
                noise_standard_deviation=noise_standard_deviation,
                number_of_steps=number_of_steps,
                random_seed=random_seed,
            )
            rms_error = calculate_steady_state_rms(
                true_positions,
                steady_state_steps,
            )
            settling_step = find_settling_step(
                true_positions,
                settling_tolerance,
            )
            results[(controller_gain, noise_standard_deviation)] = (
                rms_error,
                settling_step,
            )

    return results


def save_gain_noise_plot(
    results: dict[tuple[float, float], tuple[float, int | None]],
    gain_values: tuple[float, ...],
    noise_levels: tuple[float, ...],
    output_path: str = OUTPUT_PATH,
) -> None:
    """Save representative histories and the RMS parameter comparison."""
    figure, axes = plt.subplots(
        2,
        1,
        figsize=(8, 8),
        layout="constrained",
    )
    trajectory_noise = 0.05 if 0.05 in noise_levels else noise_levels[0]
    correction_steps = np.arange(NUMBER_OF_STEPS)

    for controller_gain in gain_values:
        _, true_positions, _ = simulate_alignment_control(
            initial_tilt_waves=INITIAL_TILT_WAVES,
            controller_gain=controller_gain,
            noise_standard_deviation=trajectory_noise,
            number_of_steps=NUMBER_OF_STEPS,
            random_seed=RANDOM_SEED,
        )
        axes[0].plot(
            correction_steps,
            true_positions,
            label=f"Gain = {controller_gain:.2f}",
        )

    axes[0].axhspan(
        -SETTLING_TOLERANCE,
        SETTLING_TOLERANCE,
        color="#16a34a",
        alpha=0.12,
        label="Settling band",
    )
    axes[0].axhline(0.0, color="black", linewidth=0.8, linestyle="--")
    axes[0].set_title(
        f"Position Histories at Noise σ = {trajectory_noise:.2f} Pixel"
    )
    axes[0].set_xlabel("Correction step")
    axes[0].set_ylabel("True position (detector pixels)")
    axes[0].grid(alpha=0.3)
    axes[0].legend()

    for noise_standard_deviation in noise_levels:
        rms_errors = [
            results[(controller_gain, noise_standard_deviation)][0]
            for controller_gain in gain_values
        ]
        axes[1].plot(
            gain_values,
            rms_errors,
            "o-",
            label=f"Noise σ = {noise_standard_deviation:.2f}",
        )

    axes[1].set_title(f"RMS Error over Final {STEADY_STATE_STEPS} Steps")
    axes[1].set_xlabel("Controller gain (waves per detector pixel)")
    axes[1].set_ylabel("RMS true-position error (detector pixels)")
    axes[1].grid(alpha=0.3)
    axes[1].legend()

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main() -> None:
    """Run the Day Four gain and measurement-noise comparison."""
    results = run_parameter_study(
        GAIN_VALUES,
        NOISE_LEVELS,
        initial_tilt_waves=INITIAL_TILT_WAVES,
        number_of_steps=NUMBER_OF_STEPS,
        random_seed=RANDOM_SEED,
        steady_state_steps=STEADY_STATE_STEPS,
        settling_tolerance=SETTLING_TOLERANCE,
    )
    save_gain_noise_plot(results, GAIN_VALUES, NOISE_LEVELS)

    print("--- Active Optical Alignment: Day Four ---")
    print(f"Initial tilt: {INITIAL_TILT_WAVES:.2f} waves")
    print(f"Recorded states: {NUMBER_OF_STEPS}")
    print(f"RMS window: final {STEADY_STATE_STEPS} states")
    print(f"Settling band: ±{SETTLING_TOLERANCE:.2f} detector pixel")
    print("Gain | Noise σ | RMS error | Settling step")
    for controller_gain in GAIN_VALUES:
        for noise_standard_deviation in NOISE_LEVELS:
            rms_error, settling_step = results[
                (controller_gain, noise_standard_deviation)
            ]
            settling_text = (
                str(settling_step)
                if settling_step is not None
                else "not settled"
            )
            print(
                f"{controller_gain:4.2f} | "
                f"{noise_standard_deviation:7.2f} | "
                f"{rms_error:9.4f} | "
                f"{settling_text}"
            )
    print(f"Plot saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
