"""Compare normal oxygen production with a one-day Mars habitat outage."""

from pathlib import Path

from mars_oxygen_budget import simulate_oxygen_budget

import matplotlib.pyplot as plt


OUTPUT_PATH = "assets/mars_oxygen_outage.png"


def save_outage_plot(
    normal_levels: list[float],
    outage_levels: list[float],
    outage_day: int,
    output_path: str = OUTPUT_PATH,
) -> None:
    """Plot stored oxygen with and without one day of lost production."""
    days = range(len(normal_levels))
    figure, axis = plt.subplots(figsize=(8, 5), layout="constrained")
    axis.plot(days, normal_levels, marker="o", markersize=3,
              label="Normal production")
    axis.plot(days, outage_levels, marker="o", markersize=3,
              label="One-day outage")
    axis.axvline(outage_day, color="gray", linestyle="--",
                 label=f"Outage on day {outage_day}")
    axis.set_title("Illustrative Mars Habitat: One-Day Oxygen Outage")
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
    """Compare the Day 2 example with production lost on day 8."""
    outage_day = 8
    normal = simulate_oxygen_budget()
    outage = simulate_oxygen_budget(outage_day=outage_day)
    save_outage_plot(normal, outage, outage_day)

    print("--- Mars Habitat: Day 3 One-Day Oxygen Outage ---")
    print("Same teaching assumptions as Day 2; production is zero on day 8 only.")
    print(f"Normal stock on day 8: {normal[outage_day]:.1f} kg")
    print(f"Outage stock on day 8: {outage[outage_day]:.1f} kg")
    print(f"Lowest outage stock: {min(outage):.1f} kg")
    print(f"Stock after 20 days: normal {normal[-1]:.1f} kg, outage {outage[-1]:.1f} kg")
    print("Production resumes on day 9, but the lost oxygen is not recovered.")
    print("This is an inventory comparison, not a cabin-safety prediction.")
    print(f"Plot saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
