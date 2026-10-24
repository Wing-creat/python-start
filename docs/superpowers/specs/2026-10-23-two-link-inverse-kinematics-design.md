# Two-Link Inverse Kinematics Design

## Intent

Extend the existing two-link arm exercise from forward kinematics to inverse
kinematics. A student should be able to choose a target `(x, y)`, calculate the
joint angles that reach it, and see why one target can have two valid arm poses.

## Scope

- Add `04_Robotics_Simulator/two_link_inverse_kinematics.py`.
- Use the same default link lengths as `two_link_arm_workspace.py`.
- Solve a planar target with the analytical cosine-rule equations.
- Return both elbow-up and elbow-down solutions when the target is reachable.
- Reject targets outside the annular workspace or inside its unreachable center.
- Plot the target and both arm poses in one clear figure under `assets/`.
- Add focused unit tests and a short README entry.

The exercise will not model motors, joint limits, collision avoidance, path
planning, three-dimensional motion, or numerical optimization.

## Approaches Considered

- **Analytical geometry (selected):** direct, accurate, and closely connected to
  the existing forward-kinematics model.
- **Angle-grid search:** simpler conceptually but approximate and unnecessarily
  slow for a two-link arm with a closed-form solution.
- **Iterative numerical solver:** useful for more complex robots but introduces
  Jacobians or optimization beyond this exercise's learning goal.

## Calculation

For link lengths `L1`, `L2` and target distance squared `r2 = x^2 + y^2`:

```text
cos(theta2) = (r2 - L1^2 - L2^2) / (2 * L1 * L2)
theta2 = +/- acos(cos(theta2))
theta1 = atan2(y, x) - atan2(L2*sin(theta2), L1 + L2*cos(theta2))
```

The public function will return angles in degrees so its output matches the
existing introductory arm scripts. A small floating-point tolerance will allow
targets exactly on the inner and outer workspace boundaries.

## Validation

Tests will feed each inverse solution back through the existing forward-
kinematics function and verify that the calculated end effector returns to the
requested target. They will also check the two solutions, workspace boundaries,
invalid link lengths, and unreachable targets. The completed script and full
test suite will be run from the repository root, and the generated plot will be
inspected.
