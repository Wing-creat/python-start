# plot_trajectory.py
import matplotlib.pyplot as plt

print("--- Plotting Free Fall Trajectory ---")

# Gravitational acceleration (m/s^2)
g = 9.8 

# Create empty lists to store our data points
time_points = []
distance_points = []

# Simulate the fall step-by-step from 0 to 5 seconds (every 1 second)
# (This uses a 'for' loop - a super important concept!)
for t in range(0, 6):
    distance = 0.5 * g * (t ** 2)
    time_points.append(t)
    distance_points.append(distance)

# Now, let's draw the graph!
plt.plot(time_points, distance_points, marker='o', color='b', linestyle='-')

# Add professional labels
plt.title("Free Fall Distance vs. Time")
plt.xlabel("Time (seconds)")
plt.ylabel("Distance fallen (meters)")
plt.grid(True) # Turn on the grid

# Show the plot window
print("Close the graph window to finish the script.")
plt.show()