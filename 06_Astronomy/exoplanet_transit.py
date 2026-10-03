"""Simple calculations for a central exoplanet transit."""

from math import acos, isfinite, pi, sqrt


def _validate_radii(star_radius: float, planet_radius: float) -> None:
    """Validate radii used by the central-transit model."""
    if not isfinite(star_radius) or not isfinite(planet_radius):
        raise ValueError("Star and planet radii must be finite.")
    if star_radius <= 0.0 or planet_radius <= 0.0:
        raise ValueError("Star and planet radii must be positive.")
    if planet_radius > star_radius:
        raise ValueError("Planet radius cannot be larger than star radius.")


def calculate_transit_depth(star_radius: float, planet_radius: float) -> float:
    """Return the blocked fraction for a central transit of uniform disks."""
    _validate_radii(star_radius, planet_radius)
    radius_ratio = planet_radius / star_radius
    return radius_ratio**2


def calculate_minimum_flux(star_radius: float, planet_radius: float) -> float:
    """Return the minimum normalized flux during a central transit."""
    transit_depth = calculate_transit_depth(star_radius, planet_radius)
    return 1.0 - transit_depth


def calculate_overlap_area(
    star_radius: float,
    planet_radius: float,
    center_separation: float,
) -> float:
    """Return the overlapping area of the star and planet disks."""
    _validate_radii(star_radius, planet_radius)
    if not isfinite(center_separation):
        raise ValueError("Center separation must be finite.")
    if center_separation < 0.0:
        raise ValueError("Center separation cannot be negative.")

    if center_separation >= star_radius + planet_radius:
        return 0.0
    if center_separation <= star_radius - planet_radius:
        return pi * planet_radius**2

    distance_squared = center_separation**2
    star_angle = acos(
        (distance_squared + star_radius**2 - planet_radius**2)
        / (2.0 * center_separation * star_radius)
    )
    planet_angle = acos(
        (distance_squared + planet_radius**2 - star_radius**2)
        / (2.0 * center_separation * planet_radius)
    )
    lens_width = sqrt(
        (-center_separation + star_radius + planet_radius)
        * (center_separation + star_radius - planet_radius)
        * (center_separation - star_radius + planet_radius)
        * (center_separation + star_radius + planet_radius)
    )

    return (
        star_radius**2 * star_angle
        + planet_radius**2 * planet_angle
        - 0.5 * lens_width
    )


def calculate_projected_separation(
    time: float,
    transit_speed: float,
    impact_parameter: float = 0.0,
) -> float:
    """Return the projected center separation at a time from mid-transit."""
    if not isfinite(time):
        raise ValueError("Time must be finite.")
    if not isfinite(transit_speed) or transit_speed <= 0.0:
        raise ValueError("Transit speed must be finite and positive.")
    if not isfinite(impact_parameter) or impact_parameter < 0.0:
        raise ValueError("Impact parameter must be finite and non-negative.")

    along_path_distance = transit_speed * time
    return sqrt(along_path_distance**2 + impact_parameter**2)


def calculate_flux_at_time(
    time: float,
    star_radius: float,
    planet_radius: float,
    transit_speed: float,
    impact_parameter: float = 0.0,
) -> float:
    """Return normalized stellar flux at a time from mid-transit."""
    center_separation = calculate_projected_separation(
        time,
        transit_speed,
        impact_parameter,
    )
    overlap_area = calculate_overlap_area(
        star_radius,
        planet_radius,
        center_separation,
    )
    star_area = pi * star_radius**2
    return 1.0 - overlap_area / star_area


if __name__ == "__main__":
    star_radius = 1.0
    planet_radius = 0.1

    transit_depth = calculate_transit_depth(star_radius, planet_radius)
    minimum_flux = calculate_minimum_flux(star_radius, planet_radius)

    print(f"Transit depth: {transit_depth:.2%}")
    print(f"Minimum normalized flux: {minimum_flux:.4f}")
