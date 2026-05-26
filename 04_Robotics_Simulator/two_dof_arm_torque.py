import math
import os

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


GRAVITY = 9.81
PAYLOAD_MASS = 5.0
LINK1_LENGTH = 0.45
LINK2_LENGTH = 0.35
LINK1_MASS = 1.2
LINK2_MASS = 0.8


def calculate_base_torque(base_angle_degrees):
    """Simple gravity torque model. The elbow stays straight."""
    angle = math.radians(base_angle_degrees)
    cos_angle = math.cos(angle)

    # Horizontal distance from the base joint to each center of mass.
    link1_center_x = (LINK1_LENGTH / 2) * cos_angle
    link2_center_x = (LINK1_LENGTH + LINK2_LENGTH / 2) * cos_angle
    payload_x = (LINK1_LENGTH + LINK2_LENGTH) * cos_angle

    return (
        LINK1_MASS * GRAVITY * link1_center_x
        + LINK2_MASS * GRAVITY * link2_center_x
        + PAYLOAD_MASS * GRAVITY * payload_x
    )


if __name__ == "__main__":
    print("=== 2-DOF Robotic Arm Torque Simulation ===\n")

    angles = list(range(0, 91))
    torques = [calculate_base_torque(angle) for angle in angles]

    plt.figure(figsize=(10, 6))
    plt.plot(angles, torques, color="#2563eb", linewidth=2.5)
    plt.title("2-DOF Robotic Arm: Base Joint Torque Curve")
    plt.xlabel("Base Joint Angle (degrees)")
    plt.ylabel("Required Base Torque (N*m)")
    plt.grid(True, linestyle="--", alpha=0.6)

    os.makedirs("assets", exist_ok=True)
    plt.savefig("assets/arm_base_torque_curve.png", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Payload mass: {PAYLOAD_MASS} kg")
    print(f"Maximum base torque: {max(torques):.2f} N*m")
    print("Plot saved to assets/arm_base_torque_curve.png")
