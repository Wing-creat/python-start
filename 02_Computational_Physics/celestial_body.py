# celestial_body.py

class Planet:
    """
    A simple class for storing basic planet data and calculating surface gravity.
    """
    G = 6.67430e-11  # Universal gravitational constant

    def __init__(self, name: str, mass: float, radius: float):
        if mass <= 0:
            raise ValueError("Error: Planet mass must be positive.")
        if radius <= 0:
            raise ValueError("Error: Planet radius must be positive.")

        self.name = name
        self.mass = mass      # in kg
        self.radius = radius  # in meters

    def get_surface_gravity(self) -> float:
        """Calculates the acceleration due to gravity on the surface: g = G*M/R^2"""
        gravity = (self.G * self.mass) / (self.radius ** 2)
        return gravity


if __name__ == "__main__":
    print("--- Celestial Surface Gravity Calculator ---")

    planets = [
        Planet("Earth", 5.972e24, 6.371e6),
        Planet("Mars", 6.39e23, 3.389e6),
        Planet("Jupiter", 1.898e27, 6.991e7),
    ]

    for planet in planets:
        print(f"{planet.name:<7} Surface Gravity: {planet.get_surface_gravity():.2f} m/s^2")

    print("-" * 45)
