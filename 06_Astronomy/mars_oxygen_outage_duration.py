"""Compare stored oxygen after outages of different lengths."""

from pathlib import Path

from mars_oxygen_budget import simulate_oxygen_budget

import matplotlib.pyplot as plt


OUTPUT_PATH = "assets/mars_oxygen_outage_duration.png"


def save_outage_duration_plot(
    durations_days: list[int],
    ending_stocks_kg: list[float],
    output_path: str = OUTPUT_PATH,
) -> None:
    """Plot stored oxygen at the end of each tested production outage."""
    figure, axis = plt.subplots(figsize=(8, 5), layout="constrained")
    axis.plot(durations_days, ending_stocks_kg, marker="o", linewidth=2)
    axis.set_title("Mars Habitat: Oxygen Remaining After an Outage")
    axis.set_xlabel("Consecutive days without production")
    axis.set_ylabel("Stored oxygen after outage (kg)")
    axis.set_xticks(durations_days)
    axis.set_xlim(left=0)
    axis.set_ylim(bottom=0)
    axis.grid(alpha=0.3)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main() -> None:
    """Compare one through four outage days beginning on day 8."""
    outage_day = 8
    durations_days = [1, 2, 3, 4]
    ending_stocks_kg = []
    for duration in durations_days:
        levels = simulate_oxygen_budget(
            outage_day=outage_day, outage_duration_days=duration
        )
        last_outage_day = outage_day + duration - 1
        ending_stocks_kg.append(levels[last_outage_day])

    save_outage_duration_plot(durations_days, ending_stocks_kg)

    print("--- Mars Habitat: Day 4 Outage Duration ---")
    print("Same teaching assumptions as Day 2; outage begins on day 8.")
    print("Outage length (days) | Stored oxygen after outage (kg)")
    for duration, stock_kg in zip(durations_days, ending_stocks_kg):
        print(f"{duration:20d} | {stock_kg:31.1f}")
    print("Three outage days leave 0.5 kg; four days reach zero inventory.")
    print("Positive stock alone does not establish safe breathing conditions.")
    print(f"Plot saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
