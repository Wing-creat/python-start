# Exoplanet Transit Study Design

## Purpose

This project will be a small, beginner-friendly astronomy study of how an
exoplanet blocks part of its star's light during a transit. It should be easy
to run, read, and explain while introducing a real geometric model one step at
a time.

The project will use synthetic examples rather than real telescope data. It
will not claim to reproduce a research pipeline or an observed exoplanet.

## Scientific Question

How do the planet-to-star radius ratio and the planet's projected position
change the amount of starlight that reaches an observer?

## Model

The initial model will make a few explicit simplifications:

- The star is a uniformly bright circular disk.
- The planet is an opaque circular disk.
- The planet follows a straight projected path across the star.
- The observed flux is normalized so that an unobscured star has flux `1.0`.
- Flux loss equals the overlapping area of the two disks divided by the
  star's area.

The first milestone only needs the central-transit result

`transit depth = (planet radius / star radius)^2`.

Later milestones will introduce disk-overlap geometry and time-dependent
motion. Limb darkening, measurement noise, orbital eccentricity, parameter
fitting, and real datasets are intentionally outside the initial project.

## Planned Structure

The completed study is expected to use these focused files:

- `06_Astronomy/exoplanet_transit.py`: reusable model and validation functions.
- `06_Astronomy/transit_study.py`: later examples and plots.
- `06_Astronomy/README.md`: short explanation, equations, and run commands.
- `tests/test_exoplanet_transit.py`: checks for the model's physical and
  numerical behavior.

Only files needed by the current milestone should be added. Empty future files
should not be created in advance.

## Data Flow

For the completed model, a study script will provide model parameters and a
sequence of times. The model will convert each time to projected center
separation, calculate the overlapping disk area, and return normalized flux.
The study script will then print key values or plot the resulting light curve.

The reusable model must return values instead of depending on printed output,
so its behavior remains easy to test.

## Input Validation

Public model functions will reject non-finite or non-positive radii. The
initial study will also require the planet radius to be no larger than the
star radius. Later position inputs must be finite, and boundary cases such as
no overlap and tangency must return physically meaningful flux values.

Errors will use clear `ValueError` messages rather than silently correcting
invalid inputs.

## Testing Strategy

Tests will grow with the model and focus on behavior that can be explained
physically:

- A central transit has depth `(planet radius / star radius)^2`.
- A radius ratio of `0.1` gives a depth of `0.01` and minimum flux of `0.99`.
- Separated disks produce normalized flux `1.0`.
- Full containment and tangent boundaries use the correct overlap limits.
- A symmetric projected path produces a symmetric light curve.
- Invalid radii and other non-finite inputs are rejected.

Floating-point comparisons will use small tolerances where exact equality is
not appropriate.

## Milestones

1. Add central-transit depth and minimum-flux functions with tests.
2. Add the area of overlap between two circular disks.
3. Convert time into projected separation and generate flux values.
4. Plot one understandable transit light curve.
5. Compare radius ratio and impact parameter in a small study.
6. Complete documentation, validation, and project-level checks.

Each milestone should stay small enough to understand and review before the
next one begins.

## Milestone 1 Scope

The first implementation milestone will add only:

- `calculate_transit_depth(star_radius, planet_radius)`;
- `calculate_minimum_flux(star_radius, planet_radius)`;
- a short runnable example showing a radius ratio of `0.1`;
- focused tests for expected values and invalid radii.

It will use the Python standard library and straightforward arithmetic. It
will not include plotting, time steps, circle-overlap geometry, a full project
README, or extra abstractions. A suitable implementation commit message is
`feat: start exoplanet transit model`.

## Success Criteria

The study succeeds if a beginning Python student can run each stage, connect
the code to the stated geometry, and explain why the light curve changes. The
code and documentation should show honest learning progress without presenting
the project as observational research.
