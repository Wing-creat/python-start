"""Track a simple oxygen-storage budget for an enclosed Mars habitat."""

import math
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUTPUT_PATH = "assets/mars_oxygen_budget.png"


def simulate_oxygen_budget(
    initial_oxygen_kg: float = 10.0,
    production_kg_per_day: float = 4.5,
    crew_size: int = 4,
    use_per_person_kg_per_day: float = 1.0,
    leak_kg_per_day: float = 0.1,
    capacity_kg: float = 20.0,
    days: int = 20,
    outage_day: int | None = None,
    outage_duration_days: int = 1,
) -> list[float]:
    """Return day-zero and end-of-day stored oxygen masses in kg.

    Each day is 24 hours, not a Martian sol. Production, use, and leakage
    are fixed daily amounts. If specified, outage_day is the first 1-based
    day with zero production. This is inventory accounting only.
    """
    amounts = (
        (initial_oxygen_kg, "Initial oxygen"),
        (production_kg_per_day, "Production"),
        (use_per_person_kg_per_day, "Use per person"),
        (leak_kg_per_day, "Leak"),
        (capacity_kg, "Capacity"),
    )
    for value, name in amounts:
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"{name} must be finite and non-negative.")
    if use_per_person_kg_per_day == 0 or capacity_kg == 0:
        raise ValueError("Use per person and capacity must be positive.")
    if initial_oxygen_kg > capacity_kg:
        raise ValueError("Initial oxygen cannot exceed capacity.")
    if not isinstance(crew_size, int) or isinstance(crew_size, bool) or crew_size <= 0:
        raise ValueError("Crew size must be a positive integer.")
    if not isinstance(days, int) or isinstance(days, bool) or days < 0:
        raise ValueError("Days must be a non-negative integer.")
    if outage_day is not None and (
        not isinstance(outage_day, int) or isinstance(outage_day, bool)
        or not 1 <= outage_day <= days
    ):
        raise ValueError("Outage day must be an integer from 1 through days.")
    if (
        not isinstance(outage_duration_days, int)
        or isinstance(outage_duration_days, bool)
        or outage_duration_days < 1
        or (outage_day is None and outage_duration_days != 1)
        or (outage_day is not None and outage_day + outage_duration_days - 1 > days)
    ):
        raise ValueError("Outage duration must be a positive integer within the simulation.")

    daily_use_kg = crew_size * use_per_person_kg_per_day
    oxygen_kg = initial_oxygen_kg
    levels = [oxygen_kg]
    for day in range(1, days + 1):
        is_outage = outage_day is not None and (
            outage_day <= day < outage_day + outage_duration_days
        )
        daily_production_kg = 0.0 if is_outage else production_kg_per_day
        oxygen_kg += daily_production_kg - daily_use_kg - leak_kg_per_day
        oxygen_kg = min(capacity_kg, max(0.0, oxygen_kg))
        levels.append(oxygen_kg)
    return levels


def save_oxygen_plot(
    low_production_levels: list[float],
    higher_production_levels: list[float],
    output_path: str = OUTPUT_PATH,
) -> None:
    """Plot two illustrative oxygen inventories over the same number of days."""
    if not low_production_levels or len(low_production_levels) != len(higher_production_levels):
        raise ValueError("Both scenarios need the same non-empty day range.")
    for level in low_production_levels + higher_production_levels:
        if not math.isfinite(level) or level < 0:
            raise ValueError("Oxygen levels must be finite and non-negative.")

    days = range(len(low_production_levels))
    figure, axis = plt.subplots(figsize=(8, 5), layout="constrained")
    axis.plot(days, low_production_levels, marker="o", markersize=3,
              label="Production: 3.5 kg/day")
    axis.plot(days, higher_production_levels, marker="o", markersize=3,
              label="Production: 4.5 kg/day")
    axis.set_title("Illustrative Mars Habitat Oxygen Storage")
    axis.set_xlabel("Earth days (24 hours each)")
    axis.set_ylabel("Stored oxygen (kg)")
    axis.set_xlim(left=0)
    axis.set_ylim(bottom=0)
    axis.grid(alpha=0.3)
    axis.legend()

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main() -> None:
    """Compare two assumed production rates with the same crew and leak."""
    low = simulate_oxygen_budget(production_kg_per_day=3.5)
    higher = simulate_oxygen_budget(production_kg_per_day=4.5)
    save_oxygen_plot(low, higher)

    print("--- Mars Habitat: Day 2 Oxygen Budget ---")
    print("Teaching assumptions: 4 people, 1 kg/person/day, 0.1 kg/day leak")
    print("Initial storage: 10 kg; tank capacity: 20 kg; 20 Earth days")
    print("Break-even production: 4.1 kg/day (consumption + leak)")
    print("Day | 3.5 kg/day production | 4.5 kg/day production")
    for day, (low_kg, higher_kg) in enumerate(zip(low, higher)):
        print(f"{day:3d} | {low_kg:21.1f} | {higher_kg:21.1f}")
    print("Zero stock means an unmet oxygen budget, not a survivability prediction.")
    print("Pressure, breathing conditions, equipment failures, and recycling are not modeled.")
    print(f"Plot saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
