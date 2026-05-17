# Computational Physics & Engineering Sandbox

> A dedicated computational sandbox for modeling physical systems, developing engineering tools, and reverse-engineering complex mechanics. 

## 👨‍💻 About This Repository
I am an incoming Engineering Physics freshman, bridging the gap between practical hardware engineering and computational simulation. Having previously competed and secured the National Grand Prize in robotics, I am now translating that hands-on mechanical intuition into Python-based analytical models.

---

## 📂 00_Archive_Basics
Foundational algorithms, syntax, and computational logic (Legacy codebase).
- `hello.py`: Initial environment configuration and testing.
- `bounding_box.py`: A foundational computer vision utility for calculating target areas.
- `cyber_oracle.py`: A logic flow exercise utilizing the `random` module and execution delays.

## 📂 01_Numerical_Methods
Algorithms for solving mathematical models through numerical approximation.
- `monte_carlo_pi.py`: Demonstrates the Monte Carlo statistical method to approximate Pi via randomized spatial distribution.
- `plot_monte_carlo.py`: Scatter plot visualization of the Monte Carlo Pi estimation using matplotlib.

## 📂 02_Computational_Physics
Core mathematical scripts and simulators for evaluating physical phenomena.
- `free_fall.py`: Multi-scenario kinematics simulator for objects in free fall, featuring robust exception handling.
- `sensor_data.py`: Simulates noise filtering and averaging for ultrasonic sensor data arrays.
- `plot_trajectory.py`: Data visualization mapping 2D projectile trajectory and kinematics using matplotlib.
- `planet_weights.py`: An interactive universal gravitation calculator for comparative planetary mass.
- `pendulum_period.py`: Period calculation for a simple pendulum.
- `kinetic_energy.py`: Classical mechanics model evaluating standard kinetic energy with strict physical constraints and test scenarios.
- `celestial_body.py`: An Object-Oriented Programming (OOP) model defining celestial objects to compute surface gravity.
- `projectile_sim.py`: A 2D kinematics simulator tracking optimal trajectory based on velocity and launch angle.
- `spring_energy.py`: Calculates elastic potential energy utilizing Hooke's Law.
- `unit_converter.py`: An engineering utility for rapid conversion between imperial and metric measurement systems.
- `aero_drag.py`: Computes aerodynamic drag force based on fluid density, velocity, and drag coefficients across different vehicle profiles (e.g., Formula 1 vs. Standard Sedan).
- `thermal_expansion.py`: Computes linear thermal expansion for mechanical materials using temperature variance and expansion coefficients.
- `ema_filter.py`: A recursive weighted-average algorithm for real-time sensor noise reduction and signal smoothing.

## 📂 03_Systems_Simulation
Deconstructing software behavior and complex mechanics using non-linear thresholds.
- `elden_ring_fall.py`: A threshold calculator simulating rigid fall-damage constraints based on specific altitude variables.
- `boss_combat_log.py`: A data parsing script tracking sequential damage output using iterative arrays.
- `weapon_database.py`: A structured data model managing variable statistics for multiple assets.

## 📂 04_Robotics_Simulator
Lightweight Python implementations of core robotics logic, extracted from practical national-level competition experience.
- `ARCHITECTURE.md`: Documentation of functional sandbox goals and fundamental control concepts.
- `robot_core.py`: Foundational classes defining 2-Wheel Differential Drive kinematics and real-time pose tracking (Odometry).

---

## 📊 Example Outputs (Visualizations)

As part of the engineering process, raw computational data is visualized to verify physical models and statistical accuracy.

### 1. Kinematics: 2D Projectile Trajectory
Visualizing the optimal flight path based on initial velocity and launch angle limits.
![Projectile Trajectory](assets/trajectory_visualization.png)

### 2. Statistics: Monte Carlo Pi Estimation
A scatter plot demonstrating the random spatial distribution used to approximate Pi.
![Monte Carlo Pi](assets/monte_carlo_visualization.png)