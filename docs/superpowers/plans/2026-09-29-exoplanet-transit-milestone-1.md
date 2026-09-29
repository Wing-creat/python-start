# Exoplanet Transit Milestone 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and test two beginner-friendly functions that calculate the depth and minimum normalized flux of a central exoplanet transit.

**Architecture:** Keep the calculation in one reusable module under `06_Astronomy`. The module will validate two radii, return numerical results instead of relying on printed output, and include a small `__main__` example for direct execution.

**Tech Stack:** Python standard library, `unittest`

**Spec:** `docs/superpowers/specs/2026-09-29-exoplanet-transit-design.md`

## Global Constraints

- Use synthetic values and do not present the project as observational research.
- Use a uniformly bright star and an opaque planet for this milestone.
- Normalize unobscured stellar flux to `1.0`.
- Calculate central-transit depth as `(planet_radius / star_radius) ** 2`.
- Reject non-finite or non-positive radii and a planet larger than its star with `ValueError`.
- Use only the Python standard library in this milestone.
- Do not add plotting, time steps, circle-overlap geometry, a full project README, or extra abstractions.

## Review Focus

- A zero star or planet radius must raise `ValueError`; covered by `test_zero_radius_is_rejected`.
- A negative star or planet radius must raise `ValueError`; covered by `test_negative_radius_is_rejected`.
- A `nan` star or planet radius must raise `ValueError`; covered by `test_nan_radius_is_rejected`.
- An infinite star or planet radius must raise `ValueError`; covered by `test_infinite_radius_is_rejected`.
- A planet radius greater than the star radius must raise `ValueError`; covered by `test_planet_larger_than_star_is_rejected`.

---

### Task 1: Central Transit Calculation

**Files:**
- Create: `06_Astronomy/exoplanet_transit.py`
- Create: `tests/test_exoplanet_transit.py`

**Interfaces:**
- Consumes: two finite positive radii expressed in the same units.
- Produces: `calculate_transit_depth(star_radius: float, planet_radius: float) -> float` and `calculate_minimum_flux(star_radius: float, planet_radius: float) -> float`.

- [ ] **Step 1: Write the failing tests for the two valid calculations**

Create `tests/test_exoplanet_transit.py` using the repository's existing `unittest` and `sys.path` import pattern. Add these assertions:

```python
def test_radius_ratio_of_point_one_has_one_percent_depth(self):
    self.assertAlmostEqual(calculate_transit_depth(1.0, 0.1), 0.01)

def test_radius_ratio_of_point_one_has_point_nine_nine_minimum_flux(self):
    self.assertAlmostEqual(calculate_minimum_flux(1.0, 0.1), 0.99)

def test_equal_radius_ratios_have_equal_depths(self):
    self.assertAlmostEqual(
        calculate_transit_depth(2.0, 0.2),
        calculate_transit_depth(1.0, 0.1),
    )
```

- [ ] **Step 2: Run the new tests and verify that the missing module causes failure**

Run: `python -m unittest tests/test_exoplanet_transit.py -v`

Expected: FAIL because `exoplanet_transit` does not exist yet.

- [ ] **Step 3: Create the two calculation functions**

Create `06_Astronomy/exoplanet_transit.py` with the exact public signatures in the Interfaces block. Use the radius-ratio equation for depth and return `1.0 - depth` for minimum flux. Add short docstrings that state the assumptions and returned quantity.

- [ ] **Step 4: Run the valid-calculation tests**

Run: `python -m unittest tests/test_exoplanet_transit.py -v`

Expected: 3 tests pass.

- [ ] **Step 5: Add failing validation tests**

Add five test methods named in Review Focus. For the first four methods, check the invalid value once as `star_radius` and once as `planet_radius`; use `0.0`, `-1.0`, `float("nan")`, and `float("inf")` respectively. Exercise both public functions across these cases. In the last method, call both public functions with `star_radius=1.0` and `planet_radius=1.1`. Every call must use `with self.assertRaises(ValueError)`.

- [ ] **Step 6: Run the validation tests and verify that they fail**

Run: `python -m unittest tests/test_exoplanet_transit.py -v`

Expected: the 5 new validation tests fail because validation is not implemented.

- [ ] **Step 7: Add shared input validation**

In `06_Astronomy/exoplanet_transit.py`, add a small private validation function used by both public functions. Use `math.isfinite`, require each radius to be greater than zero, and require `planet_radius <= star_radius`. Raise `ValueError` with a clear reason for each invalid condition.

- [ ] **Step 8: Run all milestone tests**

Run: `python -m unittest tests/test_exoplanet_transit.py -v`

Expected: 8 tests pass.

- [ ] **Step 9: Add and run the direct example**

Add an `if __name__ == "__main__":` example using `star_radius = 1.0` and `planet_radius = 0.1`. Print labeled lines that show a transit depth of `1.00%` and a minimum normalized flux of `0.9900`.

Run: `python 06_Astronomy/exoplanet_transit.py`

Expected output contains:

```text
Transit depth: 1.00%
Minimum normalized flux: 0.9900
```

- [ ] **Step 10: Run repository verification**

Run: `python -m unittest discover -s tests -v`

Expected: all repository tests pass, including the 8 new transit tests.

Run: `git diff --check`

Expected: no output.

- [ ] **Step 11: Commit the milestone**

```bash
git add 06_Astronomy/exoplanet_transit.py tests/test_exoplanet_transit.py
git commit -m "feat: start exoplanet transit model"
```
