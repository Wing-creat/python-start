"""Connect basic heat and electrical-power formulas in an ideal room model."""

import os
from math import isfinite
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUTPUT_PATH = "assets/room_heater.png"


def _require_positive(value: float, name: str) -> None:
    """Raise ValueError when a physical scale is not finite and positive."""
    if not isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and positive.")


def _require_valid_setting(heater_setting: float) -> None:
    """Require a heater setting between zero and full power."""
    if not isfinite(heater_setting) or not 0 < heater_setting <= 1:
        raise ValueError("Heater setting must be greater than 0 and at most 1.")


def calculate_air_mass(
    floor_area_m2: float,
    room_height_m: float,
    air_density_kg_m3: float = 1.2,
) -> float:
    """Return room-air mass from floor area, height, and air density."""
    _require_positive(floor_area_m2, "Floor area")
    _require_positive(room_height_m, "Room height")
    _require_positive(air_density_kg_m3, "Air density")
    room_volume_m3 = floor_area_m2 * room_height_m
    return room_volume_m3 * air_density_kg_m3


def calculate_heating_energy(
    air_mass_kg: float,
    specific_heat_j_kg_c: float,
    initial_temperature_c: float,
    target_temperature_c: float,
) -> float:
    """Return ideal heating energy using Q = m c delta-T."""
    _require_positive(air_mass_kg, "Air mass")
    _require_positive(specific_heat_j_kg_c, "Specific heat capacity")
    if not isfinite(initial_temperature_c) or not isfinite(target_temperature_c):
        raise ValueError("Temperatures must be finite.")
    if target_temperature_c <= initial_temperature_c:
        raise ValueError("Target temperature must be above initial temperature.")

    temperature_change_c = target_temperature_c - initial_temperature_c
    return air_mass_kg * specific_heat_j_kg_c * temperature_change_c


def calculate_heating_time_minutes(
    energy_j: float,
    rated_power_w: float,
    heater_setting: float = 1.0,
) -> float:
    """Return ideal heating time from t = Q / effective power."""
    _require_positive(energy_j, "Heating energy")
    _require_positive(rated_power_w, "Rated power")
    _require_valid_setting(heater_setting)
    effective_power_w = rated_power_w * heater_setting
    return energy_j / effective_power_w / 60.0


def calculate_heater_resistance(
    voltage_v: float,
    rated_power_w: float,
) -> float:
    """Return ideal heater resistance using R = V squared / P."""
    _require_positive(voltage_v, "Voltage")
    _require_positive(rated_power_w, "Rated power")
    return voltage_v**2 / rated_power_w


def calculate_ideal_temperature(
    time_min: float,
    initial_temperature_c: float,
    air_mass_kg: float,
    specific_heat_j_kg_c: float,
    rated_power_w: float,
    heater_setting: float = 1.0,
) -> float:
    """Return ideal air temperature after constant-power heating."""
    if not isfinite(time_min) or time_min < 0:
        raise ValueError("Time must be finite and non-negative.")
    if not isfinite(initial_temperature_c):
        raise ValueError("Initial temperature must be finite.")
    _require_positive(air_mass_kg, "Air mass")
    _require_positive(specific_heat_j_kg_c, "Specific heat capacity")
    _require_positive(rated_power_w, "Rated power")
    _require_valid_setting(heater_setting)

    added_energy_j = rated_power_w * heater_setting * time_min * 60.0
    temperature_change_c = added_energy_j / (
        air_mass_kg * specific_heat_j_kg_c
    )
    return initial_temperature_c + temperature_change_c


def save_heating_plot(
    times_min: list[float],
    temperatures_by_setting: dict[float, list[float]],
    target_temperature_c: float,
    output_path: str = OUTPUT_PATH,
) -> None:
    """Save ideal room-air temperature curves for several heater settings."""
    figure, axis = plt.subplots(figsize=(8, 5), layout="constrained")

    for heater_setting, temperatures_c in temperatures_by_setting.items():
        axis.plot(
            times_min,
            temperatures_c,
            label=f"{heater_setting:.0%} heater setting",
        )

    axis.axhline(
        target_temperature_c,
        color="black",
        linestyle="--",
        label=f"Target: {target_temperature_c:.0f} °C",
    )
    axis.set_title("Ideal Room-Air Heating (No Heat Loss)")
    axis.set_xlabel("Time (min)")
    axis.set_ylabel("Ideal air temperature (°C)")
    axis.grid(alpha=0.3)
    axis.legend()

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main() -> None:
    """Run the ideal room-heater example."""
    floor_area_m2 = 25.0
    room_height_m = 4.0
    air_density_kg_m3 = 1.2
    specific_heat_j_kg_c = 1005.0
    initial_temperature_c = 15.0
    target_temperature_c = 22.0
    rated_power_w = 1500.0
    voltage_v = 120.0
    heater_settings = (0.50, 0.75, 1.00)

    air_mass_kg = calculate_air_mass(
        floor_area_m2,
        room_height_m,
        air_density_kg_m3,
    )
    heating_energy_j = calculate_heating_energy(
        air_mass_kg,
        specific_heat_j_kg_c,
        initial_temperature_c,
        target_temperature_c,
    )
    resistance_ohm = calculate_heater_resistance(voltage_v, rated_power_w)

    times_min = [step * 0.25 for step in range(81)]
    temperatures_by_setting = {
        heater_setting: [
            calculate_ideal_temperature(
                time_min,
                initial_temperature_c,
                air_mass_kg,
                specific_heat_j_kg_c,
                rated_power_w,
                heater_setting,
            )
            for time_min in times_min
        ]
        for heater_setting in heater_settings
    }
    save_heating_plot(
        times_min,
        temperatures_by_setting,
        target_temperature_c,
    )

    print("--- Ideal Room Heater Study ---")
    print(f"Room: {floor_area_m2:.0f} m² floor area × {room_height_m:.0f} m high")
    print(f"Room-air mass: {air_mass_kg:.1f} kg")
    print(
        f"Heating energy for {initial_temperature_c:.0f} → "
        f"{target_temperature_c:.0f} °C: {heating_energy_j / 1000:.1f} kJ"
    )
    print(f"Ideal heater resistance at {voltage_v:.0f} V: {resistance_ohm:.2f} Ω")
    print("Setting | Effective power | Ideal heating time")
    for heater_setting in heater_settings:
        heating_time_min = calculate_heating_time_minutes(
            heating_energy_j,
            rated_power_w,
            heater_setting,
        )
        print(
            f"{heater_setting:7.0%} | "
            f"{rated_power_w * heater_setting:13.0f} W | "
            f"{heating_time_min:17.2f} min"
        )

    print("Full-power comparison at the same 4 m height:")
    for comparison_area_m2 in (15.0, 25.0, 35.0):
        comparison_mass_kg = calculate_air_mass(
            comparison_area_m2,
            room_height_m,
            air_density_kg_m3,
        )
        comparison_energy_j = calculate_heating_energy(
            comparison_mass_kg,
            specific_heat_j_kg_c,
            initial_temperature_c,
            target_temperature_c,
        )
        comparison_time_min = calculate_heating_time_minutes(
            comparison_energy_j,
            rated_power_w,
        )
        print(
            f"  {comparison_area_m2:4.0f} m² -> "
            f"{comparison_time_min:5.2f} min"
        )

    print("Assumption: only room air is heated; heat loss is ignored.")
    print(f"Plot saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
