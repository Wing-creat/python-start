# Robotics Simulator: Logic Fragments

This directory contains lightweight Python implementations of basic robotics ideas, based on concepts I have used or encountered through robotics practice and competitions.

This is not meant to be a complete robotics software stack. It is a small practice space for checking simple mechanical, physics, and control ideas in Python before thinking about real hardware.

## Core Components

### 1. Robot Kinematics (`robot_core.py`)
- **Model:** 2-wheel differential drive robot.
- **Logic:** Converts left and right wheel speeds into robot position updates.
- **Physics:** Uses simple linear and angular velocity ideas for 2D motion.

### 2. Arm Torque Simulation (`two_dof_arm_torque.py`)
- **Model:** Simple 2-DOF robotic arm with two links and a 5kg payload.
- **Logic:** Calculates the base joint torque while the arm moves from 0 to 90 degrees.
- **Physics:** Uses gravitational torque, based on each mass and its horizontal distance from the base joint.

### 3. Arm Workspace (`two_link_arm_workspace.py`)
- **Model:** Two-link planar robotic arm with unrestricted joint rotation.
- **Logic:** Uses forward kinematics to calculate reachable end-effector positions.
- **Physics:** Shows how link lengths define the minimum and maximum reach.

### 4. Signal Processing (`../02_Computational_Physics/ema_filter.py`)
- **Algorithm:** Exponential Moving Average (EMA).
- **Logic:** Smooths noisy sensor data, such as distance or encoder readings.
- **Application:** A simple first step toward cleaner robot sensor measurements.

## Project Goals
- Practice turning robotics formulas into small Python programs.
- Connect mechanics, sensors, and motion with code.
- Keep the examples understandable for early engineering physics study.
