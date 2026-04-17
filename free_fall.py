# free_fall.py
print("--- Free Fall Calculator ---")

# Gravitational acceleration constant (m/s^2)
g = 9.8 

# Assumed falling time in seconds (can be modified for testing)
time = 2.5 

# Calculate final velocity and drop distance
velocity = g * time
distance = 0.5 * g * (time ** 2)

print("Falling time: " + str(time) + " s")
print("Final velocity: " + str(velocity) + " m/s")
print("Fall distance: " + str(distance) + " m")
