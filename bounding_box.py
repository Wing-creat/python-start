# bounding_box.py
print("--- Bounding Box Area Calculation ---")

# Function to calculate the area of a detected bounding box
def calculate_area(width, height):
    return width * height

# Simulated target dimensions captured by a computer vision camera (in pixels)
box_w = 45.5
box_h = 20.0

# Execute the function to get the area
target_area = calculate_area(box_w, box_h)

print("Target width: " + str(box_w) + " px")
print("Target height: " + str(box_h) + " px")
print("Occupied area: " + str(target_area) + " sq px")
