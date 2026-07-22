# projectile_sim.py
import math
from typing import Tuple


def simulate_vacuum_trajectory(
    v0: float,
    angle_degrees: float,
    gravity: float = 9.81,
    num_points: int = 101,
) -> dict:
    """Return an ideal projectile trajectory with no air resistance."""
    if v0 < 0:
        raise ValueError("Error: Initial velocity cannot be negative.")
    if not 0 <= angle_degrees <= 90:
        raise ValueError("Error: Launch angle must be between 0 and 90 degrees.")
    if gravity <= 0:
        raise ValueError("Error: Gravity must be positive.")
    if num_points < 2:
        raise ValueError("Error: At least two trajectory points are required.")

    angle_radians = math.radians(angle_degrees)
    horizontal_velocity = v0 * math.cos(angle_radians)
    initial_vertical_velocity = v0 * math.sin(angle_radians)

    flight_time = (2 * initial_vertical_velocity) / gravity
    max_height = initial_vertical_velocity**2 / (2 * gravity)
    horizontal_range = horizontal_velocity * flight_time

    time_step = flight_time / (num_points - 1)
    times = [index * time_step for index in range(num_points)]
    x_positions = [horizontal_velocity * time for time in times]
    y_positions = [
        initial_vertical_velocity * time - 0.5 * gravity * time**2
        for time in times
    ]
    vertical_velocities = [
        initial_vertical_velocity - gravity * time for time in times
    ]

    return {
        "times": times,
        "x_positions": x_positions,
        "y_positions": y_positions,
        "x_velocities": [horizontal_velocity] * num_points,
        "y_velocities": vertical_velocities,
        "flight_time": flight_time,
        "max_height": max_height,
        "range": horizontal_range,
    }


def calculate_trajectory(v0: float, angle_degrees: float, gravity: float = 9.81) -> Tuple[float, float, float]:
    """
    Calculates key kinematics metrics of a 2D projectile trajectory.

    Assumes ideal motion with no air resistance and launch/landing at the same height.
    """
    trajectory = simulate_vacuum_trajectory(v0, angle_degrees, gravity)
    return (
        trajectory["flight_time"],
        trajectory["max_height"],
        trajectory["range"],
    )

if __name__ == "__main__":
    print("--- Projectile Motion Calculator ---")
    velocity = 50.0  # Initial velocity in m/s
    angle = 45.0     # Launch angle in degrees
    
    try:
        t, h, r = calculate_trajectory(velocity, angle)

        print("-" * 30)
        print(f"Initial Velocity : {velocity} m/s")
        print(f"Launch Angle     : {angle} degrees")
        print(f"Time of Flight   : {t:.2f} s")
        print(f"Max Height       : {h:.2f} m")
        print(f"Max Range        : {r:.2f} m")
        print("-" * 30)
    except ValueError as e:
        print(f"Calculation failed: {e}")
