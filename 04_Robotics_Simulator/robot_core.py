import math

class DifferentialBot:
    """
    A lightweight kinematic model for a 2-wheel differential drive robot.
    Extracted from high-school competition logic to demonstrate basic mobility physics.
    """
    def __init__(self, wheel_base=0.35):
        # Physical parameters (in meters)
        self.wheel_base = wheel_base  # Distance between wheels
        
        # Pose: [x, y, theta (heading in radians)]
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

    def update_odometry(self, left_vel, right_vel, dt):
        """
        Updates the robot's pose based on wheel velocities.
        
        Args:
            left_vel (float): Left wheel velocity (m/s)
            right_vel (float): Right wheel velocity (m/s)
            dt (float): Time interval (seconds)
        """
        # Linear and angular velocity calculation
        linear_v = (left_vel + right_vel) / 2.0
        angular_w = (right_vel - left_vel) / self.wheel_base
        
        # Pose integration (Simple Euler)
        self.x += linear_v * math.cos(self.theta) * dt
        self.y += linear_v * math.sin(self.theta) * dt
        self.theta += angular_w * dt
        
        # Normalize theta to [-pi, pi]
        self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta))

    def get_pose(self):
        return f"Pose: (x={self.x:.3f}, y={self.y:.3f}, θ={self.theta:.3f})"

if __name__ == "__main__":
    print("=== 🤖 Lightweight Robot Kinematics Simulator ===\n")
    
    # Initialize a competition-sized bot (35cm wheel base)
    my_bot = DifferentialBot(wheel_base=0.35)
    
    # Simulate a simple curved trajectory (Left < Right velocity)
    print("Executing a 2-second curved drive...")
    for _ in range(20): # 2 seconds at 10Hz
        my_bot.update_odometry(left_vel=0.5, right_vel=0.7, dt=0.1)
        
    print(f"Current Status: {my_bot.get_pose()}")
    print("\nStatus: Kinematic calculation complete.")