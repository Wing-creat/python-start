# Two-Link Inverse Kinematics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a small analytical inverse-kinematics study that finds and plots the valid poses of the existing two-link arm for a chosen target.

**Architecture:** One new script will contain the analytical solver and plotting function. It will reuse `calculate_end_effector()` from the existing workspace script for validation rather than create a second forward-kinematics implementation.

**Tech Stack:** Python, standard-library `math`, Matplotlib, `unittest`

**Spec:** `docs/superpowers/specs/2026-10-23-two-link-inverse-kinematics-design.md`

## Global Constraints

- Use default link lengths `0.45 m` and `0.35 m`.
- Return joint angles in degrees.
- Keep the model planar and analytical; do not add motors, joint limits, collisions, path planning, or numerical optimization.
- Keep code, plot labels, tests, and GitHub documentation in English.
- Leave implementation changes uncommitted until the user requests Git publication.

## Review Focus

- A target beyond `L1 + L2` raises `ValueError`.
- A target inside `abs(L1 - L2)` raises `ValueError`.
- Non-positive or non-finite link lengths and non-finite target coordinates raise `ValueError`.
- Targets exactly on inner and outer boundaries are accepted despite floating-point rounding.
- A normal interior target returns distinct elbow-up and elbow-down solutions.

---

### Task 1: Analytical Solver and Physics Tests

**Files:**
- Create: `04_Robotics_Simulator/two_link_inverse_kinematics.py`
- Create: `tests/test_two_link_inverse_kinematics.py`

**Interfaces:**
- Consumes: `calculate_end_effector(base_angle_degrees, elbow_angle_degrees, link1_length, link2_length)` from `two_link_arm_workspace.py`
- Produces: `solve_inverse_kinematics(target_x: float, target_y: float, link1_length: float = 0.45, link2_length: float = 0.35) -> list[tuple[float, float]]`

- [x] Write tests for an interior target, both workspace boundaries, unreachable targets, and invalid values.
- [x] Run `python3 -m unittest tests.test_two_link_inverse_kinematics -v` and verify failure because the new module is absent.
- [x] Implement the cosine-rule solver. Return two solutions for an interior point and one solution where the two poses coincide at a workspace boundary.
- [x] Feed every returned solution through existing forward kinematics and verify its endpoint matches the target within numerical tolerance.
- [x] Run the focused tests and confirm they pass.

### Task 2: Plot, Documentation, and Full Verification

**Files:**
- Modify: `04_Robotics_Simulator/two_link_inverse_kinematics.py`
- Create: `assets/two_link_inverse_kinematics.png`
- Modify: `04_Robotics_Simulator/ARCHITECTURE.md`
- Modify: `README.md`
- Test: `tests/test_two_link_inverse_kinematics.py`

**Interfaces:**
- Consumes: the list of angle pairs from `solve_inverse_kinematics()`
- Produces: `save_inverse_kinematics_plot(target_x: float, target_y: float, solutions: list[tuple[float, float]], output_path: str = "assets/two_link_inverse_kinematics.png") -> None`

- [x] Add a plot-output test using a temporary directory.
- [x] Implement the plot with the target, base, links, joints, and labels for elbow-up and elbow-down poses.
- [x] Add a small runnable example using target `(0.45, 0.35)` and print the two angle pairs.
- [x] Update the robotics architecture note and root README with purpose, formula summary, assumptions, run command, and figure.
- [x] Run `python3 04_Robotics_Simulator/two_link_inverse_kinematics.py` and inspect the generated figure.
- [x] Run `python3 -m unittest discover -s tests` and `git diff --check`, then report the uncommitted changes for review.
