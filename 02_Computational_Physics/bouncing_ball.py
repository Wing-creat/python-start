"""Simulate a ball that loses energy each time it bounces."""

import os

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUTPUT_PATH = "assets/bouncing_ball_simulation.png"


def simulate_bouncing_ball(
    initial_height: float = 10.0,
    restitution: float = 0.75,
    gravity: float = 9.81,
    time_step: float = 0.002,
    minimum_bounce_speed: float = 0.25,
    maximum_time: float = 30.0,
) -> dict:
    """Return the height of a bouncing ball at each time step."""
    if initial_height <= 0:
        raise ValueError("Initial height must be positive.")
    if not 0 <= restitution < 1:
        raise ValueError("Restitution must be between 0 and 1.")
    if gravity <= 0 or time_step <= 0:
        raise ValueError("Gravity and time step must be positive.")
    if minimum_bounce_speed < 0 or maximum_time <= 0:
        raise ValueError("Stop speed cannot be negative, and time must be positive.")

    current_time = 0.0
    height = initial_height
    velocity = 0.0
    bounce_count = 0

    times = [current_time]
    heights = [height]
    velocities = [velocity]
    peak_times = [current_time]
    peak_heights = [height]

    current_peak_time = current_time
    current_peak_height = 0.0

    while current_time < maximum_time:
        current_time += time_step
        velocity -= gravity * time_step
        height += velocity * time_step

        if height <= 0:
            height = 0.0

            # Save the highest point reached after the previous bounce.
            if bounce_count > 0:
                peak_times.append(current_peak_time)
                peak_heights.append(current_peak_height)

            rebound_speed = restitution * abs(velocity)
            if rebound_speed < minimum_bounce_speed:
                velocity = 0.0
                times.append(current_time)
                heights.append(height)
                velocities.append(velocity)
                break

            velocity = rebound_speed
            bounce_count += 1
            current_peak_time = current_time
            current_peak_height = 0.0
        elif bounce_count > 0 and height > current_peak_height:
            current_peak_time = current_time
            current_peak_height = height

        times.append(current_time)
        heights.append(height)
        velocities.append(velocity)

    return {
        "times": times,
        "heights": heights,
        "velocities": velocities,
        "peak_times": peak_times,
        "peak_heights": peak_heights,
        "bounce_count": bounce_count,
        "settled": height == 0.0 and velocity == 0.0,
    }


def save_bounce_plot(simulation: dict, output_path: str = OUTPUT_PATH) -> None:
    """Save the ball height and recorded bounce peaks."""
    plt.figure(figsize=(11, 6))
    plt.plot(
        simulation["times"],
        simulation["heights"],
        color="#2563eb",
        linewidth=2.0,
        label="Ball height",
    )
    plt.scatter(
        simulation["peak_times"],
        simulation["peak_heights"],
        color="#dc2626",
        s=28,
        label="Peak heights",
        zorder=3,
    )

    plt.title("Bouncing Ball with Energy Loss")
    plt.xlabel("Time (s)")
    plt.ylabel("Height (m)")
    plt.ylim(bottom=0)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()

    os.makedirs("assets", exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    ball_simulation = simulate_bouncing_ball(
        initial_height=10.0,
        restitution=0.75,
    )
    save_bounce_plot(ball_simulation)

    print("--- Bouncing Ball Simulation ---")
    print("Initial height       : 10.00 m")
    print("Restitution          : 0.75")
    print(f"Completed bounces    : {ball_simulation['bounce_count']}")
    print("First peak heights   :")
    for bounce_number, peak_height in enumerate(
        ball_simulation["peak_heights"][:6]
    ):
        print(f"  Peak {bounce_number}: {peak_height:.2f} m")
    print(f"Plot saved to {OUTPUT_PATH}")
