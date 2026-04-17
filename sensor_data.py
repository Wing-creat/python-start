# sensor_data.py
print("--- Sensor Data Averaging ---")

# Simulated ultrasonic distance sensor readings (in cm)
readings = [12.5, 12.8, 12.2, 13.1, 12.6]

# Calculate the sum of all readings
total = sum(readings)
# Count the number of valid data points
count = len(readings)
# Calculate the average distance
average = total / count

print("Raw data logs: " + str(readings))
print("Valid sample count: " + str(count))
print("Average distance: " + str(round(average, 2)) + " cm")
