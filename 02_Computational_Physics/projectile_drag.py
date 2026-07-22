"""Simulate projectile motion with quadratic air resistance."""

import math
from typing import Tuple

from aero_drag import calculate_drag_force


State = Tuple[float, float, float, float]


def _state_derivatives(
    state: State,
    mass_kg: float,
    drag_coefficient: float,
    area_m2: float,
    air_density: float,
    gravity: float,
) -> State:
    """Return dx/dt, dy/dt, dvx/dt, and dvy/dt for one state."""
    _, _, velocity_x, velocity_y = state
    speed = math.hypot(velocity_x, velocity_y)

    if speed == 0:
        drag_acceleration_x = 0.0
        drag_acceleration_y = 0.0
    else:
        drag_force = calculate_drag_force(
            air_density,
            speed,
            drag_coefficient,
            area_m2,
        )
        drag_acceleration = drag_force / mass_kg

        # Drag points opposite to the velocity vector.
        drag_acceleration_x = -drag_acceleration * velocity_x / speed
        drag_acceleration_y = -drag_acceleration * velocity_y / speed

    return (
        velocity_x,
        velocity_y,
        drag_acceleration_x,
        drag_acceleration_y - gravity,
    )


def _add_scaled(state: State, change: State, scale: float) -> State:
    """Return state + scale * change for the four state variables."""
    return tuple(
        value + scale * derivative
        for value, derivative in zip(state, change)
    )


def _rk4_step(
    state: State,
    time_step: float,
    mass_kg: float,
    drag_coefficient: float,
    area_m2: float,
    air_density: float,
    gravity: float,
) -> State:
    """Advance the projectile state by one fourth-order Runge-Kutta step."""
    parameters = (
        mass_kg,
        drag_coefficient,
        area_m2,
        air_density,
        gravity,
    )

    slope_1 = _state_derivatives(state, *parameters)
    slope_2 = _state_derivatives(
        _add_scaled(state, slope_1, time_step / 2),
        *parameters,
    )
    slope_3 = _state_derivatives(
        _add_scaled(state, slope_2, time_step / 2),
        *parameters,
    )
    slope_4 = _state_derivatives(
        _add_scaled(state, slope_3, time_step),
        *parameters,
    )

    return tuple(
        value
        + time_step
        * (first + 2 * second + 2 * third + fourth)
        / 6
        for value, first, second, third, fourth in zip(
            state,
            slope_1,
            slope_2,
            slope_3,
            slope_4,
        )
    )


def simulate_drag_trajectory(
    v0: float,
    angle_degrees: float,
    mass_kg: float,
    drag_coefficient: float,
    area_m2: float,
    air_density: float = 1.225,
    gravity: float = 9.81,
    time_step: float = 0.01,
    max_time: float = 60.0,
) -> dict:
    """Return a projectile trajectory with quadratic air resistance.

    The drag force is proportional to the square of speed and points in the
    opposite direction to velocity:

        F_drag = -0.5 * rho * C_d * A * |v| * v
    """
    if v0 < 0:
        raise ValueError("Initial velocity cannot be negative.")
    if not 0 <= angle_degrees <= 90:
        raise ValueError("Launch angle must be between 0 and 90 degrees.")
    if mass_kg <= 0:
        raise ValueError("Mass must be positive.")
    if drag_coefficient < 0 or area_m2 < 0 or air_density < 0:
        raise ValueError("Drag coefficient, area, and air density cannot be negative.")
    if gravity <= 0:
        raise ValueError("Gravity must be positive.")
    if time_step <= 0 or max_time <= 0:
        raise ValueError("Time step and maximum time must be positive.")

    angle_radians = math.radians(angle_degrees)
    state = (
        0.0,
        0.0,
        v0 * math.cos(angle_radians),
        v0 * math.sin(angle_radians),
    )

    times = [0.0]
    states = [state]

    while times[-1] < max_time:
        current_time = times[-1]
        current_step = min(time_step, max_time - current_time)
        next_state = _rk4_step(
            state,
            current_step,
            mass_kg,
            drag_coefficient,
            area_m2,
            air_density,
            gravity,
        )

        if next_state[1] < 0:
            # Interpolate between the final two steps to finish at ground level.
            landing_fraction = state[1] / (state[1] - next_state[1])
            landing_state = tuple(
                start + landing_fraction * (end - start)
                for start, end in zip(state, next_state)
            )
            landing_state = (
                landing_state[0],
                0.0,
                landing_state[2],
                landing_state[3],
            )
            times.append(current_time + landing_fraction * current_step)
            states.append(landing_state)
            break

        state = next_state
        times.append(current_time + current_step)
        states.append(state)
    else:
        raise RuntimeError("Projectile did not reach the ground before max_time.")

    x_positions = [current_state[0] for current_state in states]
    y_positions = [current_state[1] for current_state in states]
    x_velocities = [current_state[2] for current_state in states]
    y_velocities = [current_state[3] for current_state in states]

    return {
        "times": times,
        "x_positions": x_positions,
        "y_positions": y_positions,
        "x_velocities": x_velocities,
        "y_velocities": y_velocities,
        "flight_time": times[-1],
        "max_height": max(y_positions),
        "range": x_positions[-1],
    }


if __name__ == "__main__":
    trajectory = simulate_drag_trajectory(
        v0=50.0,
        angle_degrees=45.0,
        mass_kg=0.145,
        drag_coefficient=0.47,
        area_m2=0.0042,
    )

    print("--- Projectile Motion with Quadratic Drag ---")
    print(f"Flight Time : {trajectory['flight_time']:.2f} s")
    print(f"Max Height  : {trajectory['max_height']:.2f} m")
    print(f"Range       : {trajectory['range']:.2f} m")
