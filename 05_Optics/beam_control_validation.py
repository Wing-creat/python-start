"""Validate beam-control RMS results across several random seeds."""

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import numpy as np

from beam_feedback_control import simulate_alignment_control
from beam_gain_noise_study import calculate_steady_state_rms


OUTPUT_PATH = "assets/beam_control_validation.png"
GAIN_VALUES = (0.05, 0.20, 0.50)
NOISE_LEVELS = (0.05, 0.20)
RANDOM_SEEDS = (1, 2, 3, 4, 5)
INITIAL_TILT_WAVES = 1.5
NUMBER_OF_STEPS = 40
STEADY_STATE_STEPS = 10


def collect_rms_trials(
    gain_values: tuple[float, ...],
    noise_levels: tuple[float, ...],
    random_seeds: tuple[int, ...],
    initial_tilt_waves: float = 1.5,
    number_of_steps: int = 40,
    steady_state_steps: int = 10,
) -> dict[tuple[float, float], np.ndarray]:
    """Return one steady-state RMS value per seed for each case."""
    rms_trials = {}

    for controller_gain in gain_values:
        for noise_standard_deviation in noise_levels:
            case_trials = []
            for random_seed in random_seeds:
                _, true_positions, _ = simulate_alignment_control(
                    initial_tilt_waves=initial_tilt_waves,
                    controller_gain=controller_gain,
                    noise_standard_deviation=noise_standard_deviation,
                    number_of_steps=number_of_steps,
                    random_seed=random_seed,
                )
                case_trials.append(
                    calculate_steady_state_rms(
                        true_positions,
                        steady_state_steps,
                    )
                )
            rms_trials[(controller_gain, noise_standard_deviation)] = (
                np.asarray(case_trials)
            )

    return rms_trials


def summarize_rms_trials(
    rms_trials: dict[tuple[float, float], np.ndarray],
) -> dict[tuple[float, float], tuple[float, float]]:
    """Return mean RMS and sample standard deviation for each case."""
    summary = {}

    for case, trial_values in rms_trials.items():
        trial_array = np.asarray(trial_values, dtype=float)
        if trial_array.ndim != 1 or trial_array.size < 2:
            raise ValueError("Each case needs at least two RMS trial values.")
        if not np.all(np.isfinite(trial_array)):
            raise ValueError("RMS trial values must be finite.")
        summary[case] = (
            float(np.mean(trial_array)),
            float(np.std(trial_array, ddof=1)),
        )

    return summary


def save_validation_plot(
    summary: dict[tuple[float, float], tuple[float, float]],
    gain_values: tuple[float, ...],
    noise_levels: tuple[float, ...],
    output_path: str = OUTPUT_PATH,
) -> None:
    """Save mean RMS values with sample-standard-deviation error bars."""
    figure, axis = plt.subplots(figsize=(8, 5), layout="constrained")

    for noise_standard_deviation in noise_levels:
        mean_values = [
            summary[(controller_gain, noise_standard_deviation)][0]
            for controller_gain in gain_values
        ]
        standard_deviations = [
            summary[(controller_gain, noise_standard_deviation)][1]
            for controller_gain in gain_values
        ]
        axis.errorbar(
            gain_values,
            mean_values,
            yerr=standard_deviations,
            marker="o",
            capsize=4,
            label=f"Noise σ = {noise_standard_deviation:.2f}",
        )

    axis.set_title("Beam-Control RMS across Five Random Seeds")
    axis.set_xlabel("Controller gain (waves per detector pixel)")
    axis.set_ylabel("Mean RMS true-position error (detector pixels)")
    axis.grid(alpha=0.3)
    axis.legend()

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main() -> None:
    """Run the Day Five multi-seed control validation."""
    rms_trials = collect_rms_trials(
        GAIN_VALUES,
        NOISE_LEVELS,
        RANDOM_SEEDS,
        initial_tilt_waves=INITIAL_TILT_WAVES,
        number_of_steps=NUMBER_OF_STEPS,
        steady_state_steps=STEADY_STATE_STEPS,
    )
    summary = summarize_rms_trials(rms_trials)
    save_validation_plot(summary, GAIN_VALUES, NOISE_LEVELS)

    print("--- Active Optical Alignment: Day Five ---")
    print(f"Random seeds: {RANDOM_SEEDS}")
    print(f"RMS window: final {STEADY_STATE_STEPS} states")
    print("Gain | Noise σ | Mean RMS | Sample σ")
    for controller_gain in GAIN_VALUES:
        for noise_standard_deviation in NOISE_LEVELS:
            mean_rms, sample_standard_deviation = summary[
                (controller_gain, noise_standard_deviation)
            ]
            print(
                f"{controller_gain:4.2f} | "
                f"{noise_standard_deviation:7.2f} | "
                f"{mean_rms:8.4f} | "
                f"{sample_standard_deviation:8.4f}"
            )
    print(f"Plot saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
