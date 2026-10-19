"""Estimate battery runtime for a device drawing constant power."""

from math import isfinite


def calculate_runtime_hours(
    energy_wh: float,
    power_w: float,
    efficiency: float = 1.0,
) -> float:
    """Return runtime in hours from usable energy divided by power."""
    if not isfinite(energy_wh) or energy_wh <= 0:
        raise ValueError("Battery energy must be finite and positive.")
    if not isfinite(power_w) or power_w <= 0:
        raise ValueError("Device power must be finite and positive.")
    if not isfinite(efficiency) or not 0 < efficiency <= 1:
        raise ValueError("Efficiency must be greater than zero and at most one.")
    return energy_wh * efficiency / power_w


if __name__ == "__main__":
    # Illustrative values for a constant-power device.
    hours = calculate_runtime_hours(100.0, 20.0, 0.8)
    print("--- Simple Battery Runtime ---")
    print("Battery: 100 Wh | Device: 20 W | Efficiency: 80%")
    print(f"Estimated runtime: {hours:.1f} hours")
