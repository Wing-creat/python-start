# celestial_body.py

class Planet:
    """
    A blueprint for creating celestial bodies. 
    In Engineering Physics, we call this encapsulation.
    """
    # Universal Gravitational Constant (G)
    G = 6.67430e-11 

    def __init__(self, name, mass, radius):
        # The __init__ method is the "constructor". 
        # It sets up the unique stats for each new planet we create.
        self.name = name
        self.mass = mass      # in kg
        self.radius = radius  # in meters

    def get_surface_gravity(self):
        """Calculates the acceleration due to gravity on the surface: g = G*M/R^2"""
        gravity = (self.G * self.mass) / (self.radius ** 2)
        return gravity

print(f"--- 🪐 Celestial Gravity Lab ---")

# Now, we use the blueprint to create REAL objects!
# Creating Earth
earth = Planet("Earth", 5.972e24, 6.371e6)
# Creating Mars
mars = Planet("Mars", 6.39e23, 3.389e6)
# Let's create Jupiter just for fun!
jupiter = Planet("Jupiter", 1.898e27, 6.991e7)

print(f"{earth.name} Surface Gravity: {earth.get_surface_gravity():.2f} m/s^2")
print(f"{mars.name}  Surface Gravity: {mars.get_surface_gravity():.2f} m/s^2")
print(f"{jupiter.name} Surface Gravity: {jupiter.get_surface_gravity():.2f} m/s^2")
print("-" * 35)