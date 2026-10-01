"""Simple calculations for a central exoplanet transit."""

from math import isfinite


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


if __name__ == "__main__":
    star_radius = 1.0
    planet_radius = 0.1

    transit_depth = calculate_transit_depth(star_radius, planet_radius)
    minimum_flux = calculate_minimum_flux(star_radius, planet_radius)

    print(f"Transit depth: {transit_depth:.2%}")
    print(f"Minimum normalized flux: {minimum_flux:.4f}")
