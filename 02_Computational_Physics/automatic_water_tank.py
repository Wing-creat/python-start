"""Simulate an automatic pump that keeps a water tank within set levels."""

import os

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUTPUT_PATH = "assets/automatic_water_tank.png"


def simulate_water_tank(
    initial_level_m: float = 0.65,
    tank_height_m: float = 1.0,
    low_level_m: float = 0.30,
    high_level_m: float = 0.75,
    pump_rate_m_per_s: float = 0.025,
    usage_rate_m_per_s: float = 0.008,
    duration_s: float = 300.0,
    time_step_s: float = 0.5,
) -> dict:
    """Return the water level and pump state during an automatic cycle."""
    if tank_height_m <= 0:
        raise ValueError("Tank height must be positive.")
    if not 0 <= initial_level_m <= tank_height_m:
        raise ValueError("Initial level must be inside the tank.")
    if not 0 <= low_level_m < high_level_m <= tank_height_m:
        raise ValueError("Level thresholds must be ordered inside the tank.")
    if usage_rate_m_per_s < 0 or pump_rate_m_per_s <= usage_rate_m_per_s:
        raise ValueError("The pump rate must be greater than the usage rate.")
    if duration_s <= 0 or time_step_s <= 0:
        raise ValueError("Duration and time step must be positive.")

    current_time = 0.0
    water_level = initial_level_m
    pump_on = water_level <= low_level_m
    pump_start_count = 1 if pump_on else 0

    times = [current_time]
    water_levels = [water_level]
    pump_states = [pump_on]
    switch_times = []
    switch_levels = []
    switch_states = []

    while current_time < duration_s:
        step = min(time_step_s, duration_s - current_time)
        level_change_rate = -usage_rate_m_per_s
        if pump_on:
            level_change_rate += pump_rate_m_per_s

        water_level += level_change_rate * step
        water_level = min(tank_height_m, max(0.0, water_level))
        current_time += step

        previous_pump_state = pump_on
        if pump_on and water_level >= high_level_m:
            pump_on = False
        elif not pump_on and water_level <= low_level_m:
            pump_on = True
            pump_start_count += 1

        if pump_on != previous_pump_state:
            switch_times.append(current_time)
            switch_levels.append(water_level)
            switch_states.append(pump_on)

        times.append(current_time)
        water_levels.append(water_level)
        pump_states.append(pump_on)

    return {
        "times": times,
        "water_levels": water_levels,
        "pump_states": pump_states,
        "switch_times": switch_times,
        "switch_levels": switch_levels,
        "switch_states": switch_states,
        "pump_start_count": pump_start_count,
        "low_level_m": low_level_m,
        "high_level_m": high_level_m,
        "tank_height_m": tank_height_m,
    }


def save_water_tank_plot(simulation: dict, output_path: str = OUTPUT_PATH) -> None:
    """Save the water level and pump state on two aligned graphs."""
    figure, (level_axis, pump_axis) = plt.subplots(
        2,
        1,
        figsize=(11, 7),
        sharex=True,
        gridspec_kw={"height_ratios": [3, 1]},
    )

    level_axis.plot(
        simulation["times"],
        simulation["water_levels"],
        color="#2563eb",
        linewidth=2.2,
        label="Water level",
    )
    level_axis.axhline(
        simulation["high_level_m"],
        color="#16a34a",
        linestyle="--",
        label="Pump-off level",
    )
    level_axis.axhline(
        simulation["low_level_m"],
        color="#dc2626",
        linestyle="--",
        label="Pump-on level",
    )
    level_axis.set_title("Automatic Water Tank Level Control")
    level_axis.set_ylabel("Water Level (m)")
    level_axis.set_ylim(0, simulation["tank_height_m"])
    level_axis.grid(True, linestyle="--", alpha=0.4)
    level_axis.legend(loc="upper right")

    pump_values = [int(pump_on) for pump_on in simulation["pump_states"]]
    pump_axis.step(
        simulation["times"],
        pump_values,
        where="post",
        color="#7c3aed",
        linewidth=2.0,
    )
    pump_axis.set_xlabel("Time (s)")
    pump_axis.set_ylabel("Pump")
    pump_axis.set_yticks([0, 1], labels=["OFF", "ON"])
    pump_axis.set_ylim(-0.2, 1.2)
    pump_axis.grid(True, linestyle="--", alpha=0.4)

    figure.tight_layout()
    os.makedirs("assets", exist_ok=True)
    figure.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    tank_simulation = simulate_water_tank()
    save_water_tank_plot(tank_simulation)

    print("--- Automatic Water Tank ---")
    print("Tank height       : 1.00 m")
    print("Pump turns ON at : 0.30 m")
    print("Pump turns OFF at: 0.75 m")
    print("Pump rate        : 0.025 m/s")
    print("Usage rate       : 0.008 m/s")
    print(f"Pump starts      : {tank_simulation['pump_start_count']}")
    print(
        "Observed level   : "
        f"{min(tank_simulation['water_levels']):.3f} m to "
        f"{max(tank_simulation['water_levels']):.3f} m"
    )
    print(f"Plot saved to {OUTPUT_PATH}")
