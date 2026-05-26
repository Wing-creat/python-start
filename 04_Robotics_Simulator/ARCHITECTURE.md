# 🤖 Robotics Simulator: Logic Fragments

This directory contains lightweight Python implementations of core robotics logic, extracted from my practical experience in national-level robotics competitions. 

Instead of a complex, full-scale system, these scripts serve as a functional sandbox to verify fundamental mechanical and control concepts before hardware implementation.

## 📂 Core Components

### 1. Robot Kinematics (`robot_core.py`)
- **Model:** 2-Wheel Differential Drive (The standard for most competition bots).
- **Logic:** Translating independent wheel velocities into real-time pose tracking (Odometry).
- **Physics:** Utilizing linear and angular velocity integration for 2D position estimation.

### 2. Arm Torque Simulation (`two_dof_arm_torque.py`)
- **Model:** Simple 2-DOF robotic arm with two links and a 5kg payload.
- **Logic:** Calculates the base joint torque while the arm moves from 0 to 90 degrees.
- **Physics:** Uses gravitational torque, based on each mass and its horizontal distance from the base joint.

### 3. Signal Processing (`../02_Computational_Physics/ema_filter.py`)
- **Algorithm:** Exponential Moving Average (EMA).
- **Logic:** Real-time smoothing of noisy sensor data (e.g., ultrasonic or encoder readings).
- **Application:** Low-latency filtering crucial for high-speed obstacle avoidance.

## 🎯 Project Goals
- Maintain a modular library of competition-tested logic.
- Bridge the gap between mechanical hardware design and firmware control.
- Verify mathematical models in a risk-free software environment.
