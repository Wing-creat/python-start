"""Visualize the reachable workspace of a simple two-link robotic arm."""

import math
import os

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


LINK1_LENGTH = 0.45
LINK2_LENGTH = 0.35
OUTPUT_PATH = "assets/two_link_arm_workspace.png"


def calculate_end_effector(
    base_angle_degrees: float,
    elbow_angle_degrees: float,
    link1_length: float = LINK1_LENGTH,
    link2_length: float = LINK2_LENGTH,
) -> tuple:
    """Return the end-effector position from two joint angles."""
    if link1_length <= 0 or link2_length <= 0:
        raise ValueError("Link lengths must be positive.")

    base_angle = math.radians(base_angle_degrees)
    combined_angle = math.radians(base_angle_degrees + elbow_angle_degrees)

    x_position = (
        link1_length * math.cos(base_angle)
        + link2_length * math.cos(combined_angle)
    )
    y_position = (
        link1_length * math.sin(base_angle)
        + link2_length * math.sin(combined_angle)
    )

    return x_position, y_position


def generate_workspace(
    angle_step_degrees: int = 5,
    link1_length: float = LINK1_LENGTH,
    link2_length: float = LINK2_LENGTH,
) -> dict:
    """Calculate reachable points while both joints rotate through 360 degrees."""
    if angle_step_degrees <= 0:
        raise ValueError("Angle step must be positive.")
    if link1_length <= 0 or link2_length <= 0:
        raise ValueError("Link lengths must be positive.")

    joint_angles = range(-180, 181, angle_step_degrees)
    x_positions = []
    y_positions = []
    elbow_angles = []

    for base_angle in joint_angles:
        for elbow_angle in joint_angles:
            x_position, y_position = calculate_end_effector(
                base_angle,
                elbow_angle,
                link1_length,
                link2_length,
            )
            x_positions.append(x_position)
            y_positions.append(y_position)
            elbow_angles.append(elbow_angle)

    return {
        "x_positions": x_positions,
        "y_positions": y_positions,
        "elbow_angles": elbow_angles,
        "minimum_reach": abs(link1_length - link2_length),
        "maximum_reach": link1_length + link2_length,
    }


def save_workspace_plot(workspace: dict, output_path: str = OUTPUT_PATH) -> None:
    """Save a plot of reachable end-effector positions."""
    figure, axis = plt.subplots(figsize=(8, 8))
    points = axis.scatter(
        workspace["x_positions"],
        workspace["y_positions"],
        c=workspace["elbow_angles"],
        cmap="viridis",
        s=8,
        alpha=0.55,
    )

    outer_boundary = plt.Circle(
        (0.0, 0.0),
        workspace["maximum_reach"],
        fill=False,
        color="#dc2626",
        linestyle="--",
        linewidth=1.8,
        label="Maximum reach",
    )
    inner_boundary = plt.Circle(
        (0.0, 0.0),
        workspace["minimum_reach"],
        fill=False,
        color="#ea580c",
        linestyle=":",
        linewidth=1.8,
        label="Minimum reach",
    )
    axis.add_patch(outer_boundary)
    axis.add_patch(inner_boundary)
    axis.scatter(0.0, 0.0, color="#111827", s=55, label="Arm base", zorder=3)

    plot_limit = workspace["maximum_reach"] * 1.12
    axis.set_xlim(-plot_limit, plot_limit)
    axis.set_ylim(-plot_limit, plot_limit)
    axis.set_aspect("equal", adjustable="box")
    axis.set_title("Two-Link Robotic Arm Reachable Workspace")
    axis.set_xlabel("x position (m)")
    axis.set_ylabel("y position (m)")
    axis.grid(True, linestyle="--", alpha=0.35)
    axis.legend(loc="upper right")

    color_bar = figure.colorbar(points, ax=axis, shrink=0.82)
    color_bar.set_label("Elbow angle (degrees)")
    figure.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    figure.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    arm_workspace = generate_workspace(angle_step_degrees=5)
    save_workspace_plot(arm_workspace)

    print("--- Two-Link Robotic Arm Workspace ---")
    print(f"Link lengths        : {LINK1_LENGTH:.2f} m and {LINK2_LENGTH:.2f} m")
    print(f"Configurations      : {len(arm_workspace['x_positions']):,}")
    print(f"Minimum reach       : {arm_workspace['minimum_reach']:.2f} m")
    print(f"Maximum reach       : {arm_workspace['maximum_reach']:.2f} m")
    print(f"Plot saved to {OUTPUT_PATH}")
