# Active Optical Alignment Day One Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a noise-free calibration from horizontal wavefront tilt to measured far-field beam position.

**Architecture:** A new optics script will reuse the existing aperture, tilt, and FFT functions. It will measure the horizontal intensity centroid inside a finite detector window, simulate several tilt values, fit a straight calibration line, and save one explanatory plot.

**Tech Stack:** Python, NumPy, Matplotlib, unittest

**Spec:** `docs/superpowers/specs/2026-10-28-feedback-control-under-noise-design.md`

## Global Constraints

- Keep the model one-dimensional in horizontal beam position for Day One.
- Report beam position in detector pixels, not physical distance or angle.
- Use the existing NumPy and Matplotlib dependencies; add no dependency.
- Do not add noise, feedback control, PID control, or robotics behavior yet.
- Keep code and documentation readable for an introductory Engineering Physics portfolio.
- Do not commit until the user has reviewed the completed Day One diff.

## Review Focus

- A zero-total detector window must raise `ValueError` instead of dividing by zero; Task 1 tests this.
- Negative or non-finite intensity must be rejected as unphysical input; Task 1 tests this.
- A detector half-width that does not fit the intensity array must be rejected; Task 1 tests this.
- Tilt inputs must be a non-empty finite one-dimensional array; Task 1 tests this.
- A custom plot path must create its parent directory; Task 2 tests this.

---

### Task 1: Beam centroid and noise-free calibration

**Files:**
- Create: `05_Optics/beam_alignment.py`
- Create: `tests/test_active_optical_alignment.py`

**Interfaces:**
- Consumes: `create_coordinate_grid`, `create_circular_aperture`, `create_tilted_field`, and `calculate_far_field_intensity` from `05_Optics/fourier_optics.py`.
- Produces: `measure_horizontal_centroid(intensity: np.ndarray, detector_half_width: int = 30) -> float`.
- Produces: `simulate_beam_positions(tilt_values: np.ndarray, grid_size: int = 257, physical_size: float = 2.0, aperture_radius: float = 0.35, detector_half_width: int = 30) -> np.ndarray`.
- Produces: `fit_tilt_calibration(tilt_values: np.ndarray, beam_positions: np.ndarray) -> tuple[float, float]`, returning slope and intercept in that order.

- [ ] **Step 1: Write failing centroid tests**

Add tests showing that a hand-checked synthetic pattern has a centroid of
`0.75` pixel, a centered pattern measures `0.0`, and invalid intensity or
detector-window inputs raise `ValueError`.

- [ ] **Step 2: Run the centroid tests and verify RED**

Run: `.venv/bin/python -m unittest tests.test_active_optical_alignment -v`

Expected: import failure because `beam_alignment.py` does not exist.

- [ ] **Step 3: Implement the minimal centroid function**

Use a square window of side `2 * detector_half_width + 1` around the array
center. Sum intensity over rows and calculate the horizontal weighted mean in
pixel-offset coordinates.

- [ ] **Step 4: Run the centroid tests and verify GREEN**

Run: `.venv/bin/python -m unittest tests.test_active_optical_alignment -v`

Expected: all current tests pass.

- [ ] **Step 5: Write failing simulation and calibration tests**

Add tests that verify zero tilt is centered, `-1.0` and `+1.0` waves produce
opposite displacements, `2.0` waves has a larger displacement magnitude than
`1.0` wave, invalid tilt arrays raise `ValueError`, and the calibration fit
recovers slope `3.0` and intercept `0.5` from hand-written sample points.

- [ ] **Step 6: Run the new tests and verify RED**

Run: `.venv/bin/python -m unittest tests.test_active_optical_alignment -v`

Expected: failures because the simulation and fit functions do not exist.

- [ ] **Step 7: Implement the minimal simulation and calibration functions**

Create the grid and aperture once, apply each requested tilt, calculate its
far-field intensity, and call `measure_horizontal_centroid`. Validate the
calibration arrays before fitting them with `np.polyfit`.

- [ ] **Step 8: Run Task 1 tests and verify GREEN**

Run: `.venv/bin/python -m unittest tests.test_active_optical_alignment -v`

Expected: all Task 1 tests pass.

Commit: deferred until user review.

---

### Task 2: Calibration figure and learning documentation

**Files:**
- Modify: `05_Optics/beam_alignment.py`
- Modify: `tests/test_active_optical_alignment.py`
- Modify: `05_Optics/README.md`
- Create by running the script: `assets/beam_tilt_calibration.png`

**Interfaces:**
- Consumes: all three functions produced by Task 1.
- Produces: `save_calibration_plot(tilt_values: np.ndarray, beam_positions: np.ndarray, slope: float, intercept: float, output_path: str = "assets/beam_tilt_calibration.png") -> None`.
- Produces: a root-runnable script that uses 17 tilt values from `-2.0` to `2.0` waves and prints the fitted calibration.

- [ ] **Step 1: Write a failing custom-output-path test**

Use a temporary nested directory and assert that `save_calibration_plot`
creates the requested PNG.

- [ ] **Step 2: Run the plot test and verify RED**

Run: `.venv/bin/python -m unittest tests.test_active_optical_alignment -v`

Expected: failure because `save_calibration_plot` does not exist.

- [ ] **Step 3: Implement the plot and script entry point**

Plot measured points and their fitted line, label both axes with waves and
detector pixels, and state in the title that this is the noise-free baseline.
The script must print slope, intercept, the zero-tilt position, and the output
path.

- [ ] **Step 4: Run the focused tests and verify GREEN**

Run: `.venv/bin/python -m unittest tests.test_active_optical_alignment -v`

Expected: all focused tests pass.

- [ ] **Step 5: Run the script and inspect its numerical output**

Run: `.venv/bin/python 05_Optics/beam_alignment.py`

Expected: finite slope and intercept, a zero-tilt position close to zero, and
`assets/beam_tilt_calibration.png` created.

- [ ] **Step 6: Update the optics README**

Add `beam_alignment.py` to the study sequence and run commands. Explain that
Day One establishes a finite-window centroid calibration in detector pixels,
and that noise and feedback are intentionally deferred.

- [ ] **Step 7: Run fresh verification**

Run: `.venv/bin/python -m unittest discover -s tests -v`

Expected: the full repository test suite passes with no failures.

Run: `git diff --check`

Expected: no output and exit status 0.

Commit: deferred until user review.
