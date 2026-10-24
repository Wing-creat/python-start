"""Solve a simple two-link planar arm with analytical geometry."""

import math
import os

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


LINK1_LENGTH = 0.45
LINK2_LENGTH = 0.35
OUTPUT_PATH = "assets/two_link_inverse_kinematics.png"


def solve_inverse_kinematics(
    target_x: float,
    target_y: float,
    link1_length: float = LINK1_LENGTH,
    link2_length: float = LINK2_LENGTH,
) -> list[tuple[float, float]]:
    """Return reachable (base angle, elbow angle) pairs in degrees."""
    values = (target_x, target_y, link1_length, link2_length)
    if not all(math.isfinite(value) for value in values):
        raise ValueError("Target coordinates and link lengths must be finite.")
    if link1_length <= 0 or link2_length <= 0:
        raise ValueError("Link lengths must be positive.")

    target_distance = math.hypot(target_x, target_y)
    minimum_reach = abs(link1_length - link2_length)
    maximum_reach = link1_length + link2_length
    tolerance = 1e-12 * max(1.0, maximum_reach)
    if target_distance < minimum_reach - tolerance or target_distance > maximum_reach + tolerance:
        raise ValueError("Target is outside the arm's reachable workspace.")

    if math.isclose(target_distance, maximum_reach, abs_tol=tolerance):
        cosine_elbow = 1.0
    elif math.isclose(target_distance, minimum_reach, abs_tol=tolerance):
        cosine_elbow = -1.0
    else:
        cosine_elbow = (
            target_distance**2 - link1_length**2 - link2_length**2
        ) / (2 * link1_length * link2_length)
        cosine_elbow = max(-1.0, min(1.0, cosine_elbow))
    elbow_magnitude = math.acos(cosine_elbow)

    elbow_angles = [elbow_magnitude]
    if not math.isclose(math.sin(elbow_magnitude), 0.0, abs_tol=1e-12):
        elbow_angles.append(-elbow_magnitude)

    solutions = []
    for elbow_angle in elbow_angles:
        base_angle = math.atan2(target_y, target_x) - math.atan2(
            link2_length * math.sin(elbow_angle),
            link1_length + link2_length * math.cos(elbow_angle),
        )
        solutions.append((math.degrees(base_angle), math.degrees(elbow_angle)))

    return solutions


def save_inverse_kinematics_plot(
    target_x: float,
    target_y: float,
    solutions: list[tuple[float, float]],
    output_path: str = OUTPUT_PATH,
) -> None:
    """Plot each inverse-kinematics solution for the default arm lengths."""
    figure, axis = plt.subplots(figsize=(7, 7))
    colors = ("#2563eb", "#ea580c")

    for index, (base_degrees, elbow_degrees) in enumerate(solutions):
        base_angle = math.radians(base_degrees)
        elbow_angle = math.radians(elbow_degrees)
        elbow_x = LINK1_LENGTH * math.cos(base_angle)
        elbow_y = LINK1_LENGTH * math.sin(base_angle)
        side_of_target_line = target_x * elbow_y - target_y * elbow_x
        label = "Elbow up" if side_of_target_line > 0 else "Elbow down"
        if len(solutions) == 1:
            label = "Boundary solution"
        axis.plot(
            [0.0, elbow_x, target_x],
            [0.0, elbow_y, target_y],
            marker="o",
            linewidth=2.5,
            color=colors[index % len(colors)],
            label=f"{label}: ({base_degrees:.1f}°, {elbow_degrees:.1f}°)",
        )

    axis.scatter(target_x, target_y, marker="*", s=180, color="#dc2626", label="Target")
    axis.scatter(0.0, 0.0, s=55, color="#111827", label="Arm base", zorder=3)
    plot_limit = (LINK1_LENGTH + LINK2_LENGTH) * 1.1
    axis.set_xlim(-plot_limit, plot_limit)
    axis.set_ylim(-plot_limit, plot_limit)
    axis.set_aspect("equal", adjustable="box")
    axis.set_title("Two-Link Arm Inverse Kinematics")
    axis.set_xlabel("x position (m)")
    axis.set_ylabel("y position (m)")
    axis.grid(alpha=0.3)
    axis.legend(loc="lower left")
    figure.tight_layout()

    output_directory = os.path.dirname(output_path)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)
    figure.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    target_x = 0.45
    target_y = 0.35
    solutions = solve_inverse_kinematics(target_x, target_y)
    save_inverse_kinematics_plot(target_x, target_y, solutions)

    print("--- Two-Link Arm Inverse Kinematics ---")
    print(f"Target: ({target_x:.2f}, {target_y:.2f}) m")
    for index, (base_angle, elbow_angle) in enumerate(solutions, start=1):
        print(f"Solution {index}: base = {base_angle:.2f}°, elbow = {elbow_angle:.2f}°")
    print(f"Plot saved to {OUTPUT_PATH}")
