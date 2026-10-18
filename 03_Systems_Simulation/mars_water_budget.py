"""Track an illustrative Mars habitat's water inventory with ideal recycling."""

from math import isfinite


def simulate_water_budget(
    initial_water_l: float = 100.0,
    crew_size: int = 4,
    water_use_per_person_l: float = 5.0,
    recycling_fraction: float = 0.8,
    days: int = 10,
) -> list[float]:
    """Return day-zero stock and daily stocks, stopping when water runs out.

    Days are 24-hour accounting periods, not Martian sols. Recovery is assumed
    immediate; only net losses are tracked. A zero entry means the budget was
    exhausted during or at the end of that period, not a full day supplied.
    """
    if not isfinite(initial_water_l) or initial_water_l <= 0:
        raise ValueError("Initial water must be finite and positive.")
    if not isinstance(crew_size, int) or isinstance(crew_size, bool) or crew_size <= 0:
        raise ValueError("Crew size must be a positive integer.")
    if not isfinite(water_use_per_person_l) or water_use_per_person_l <= 0:
        raise ValueError("Daily water use must be finite and positive.")
    if not isfinite(recycling_fraction) or not 0 <= recycling_fraction <= 1:
        raise ValueError("Recycling fraction must be between zero and one.")
    if not isinstance(days, int) or isinstance(days, bool) or days < 0:
        raise ValueError("Days must be a non-negative integer.")

    daily_use_l = crew_size * water_use_per_person_l
    daily_loss_l = daily_use_l * (1 - recycling_fraction)
    remaining_water_l = initial_water_l
    water_levels_l = [remaining_water_l]

    for _ in range(days):
        remaining_water_l = max(0.0, remaining_water_l - daily_loss_l)
        water_levels_l.append(remaining_water_l)
        if remaining_water_l == 0:
            break

    return water_levels_l


if __name__ == "__main__":
    # Teaching assumptions, not measured Mars habitat requirements.
    water_levels = simulate_water_budget()
    print("--- Mars Habitat: Simple Water Budget ---")
    print("Assumed: 4 people, 100 L initial stock, 5 L/person per 24 h")
    print("Ideal immediate recovery: 80%; net loss: 4 L per 24 h")
    print("Period | Remaining water (L)")
    for day, water_l in enumerate(water_levels):
        print(f"{day:6d} | {water_l:19.1f}")
    if water_levels[-1] == 0:
        print("Budget exhausted within the last period; it is not a full supplied day.")
    print("Inventory accounting only: water quality and other survival needs are not modeled.")
