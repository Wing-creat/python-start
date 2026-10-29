# Feedback Control Under Noise Design

## Intent

Build a multi-day Engineering Physics study around one practical question:
how well can a simple feedback controller correct a measured error when the
measurement contains noise?

The study will use two independent case studies:

1. active optical alignment of a tilted beam;
2. trajectory tracking with a two-link robotic arm.

The two cases will share the same scientific workflow and comparison metrics,
but they will remain in their existing subject folders. This keeps the code
easy to follow and avoids creating a general control framework before it is
actually needed.

## Learning Goals

- Turn an existing physics model into a measurable system.
- Separate the true system state from a noisy sensor reading.
- Apply a simple proportional feedback correction.
- Compare accuracy, noise sensitivity, and settling behavior.
- Validate numerical results instead of relying only on plots.
- Show gradual, honest progress through small milestone commits.

This is a student learning project. It explores concepts related to optical
wavefront control and robotics feedback, but it does not claim to reproduce a
research laboratory instrument or advanced adaptive-optics system.

## Approaches Considered

### 1. Two independent case studies with one experiment method (selected)

Keep the optical model in `05_Optics` and the arm model in
`04_Robotics_Simulator`. Each case will use the same sequence:

```text
system model -> measurement -> noise -> feedback -> parameter sweep -> metrics
```

This approach makes the connection between the projects visible without
hiding the physics inside reusable abstractions.

### 2. A shared controller framework

A common controller class could be reused by both studies, but it would add
structure before the two problems are understood. It may become useful later,
but it is not part of the initial project.

### 3. One combined robot-and-optics simulation

A robot could be presented as the device that moves an optical component. That
would connect both subjects physically, but it would introduce artificial
assumptions and make it harder to tell which model caused each result.

## Case Study A: Active Optical Alignment

### Physical model

The study will reuse the existing Fourier-optics functions. A horizontal phase
tilt across the circular aperture shifts the far-field diffraction pattern.
The beam position will be measured with an intensity-weighted centroid:

```text
x_centroid = sum(x_pixel * intensity) / sum(intensity)
```

The first version will use only one horizontal axis. This matches the current
tilt model and keeps the feedback behavior easy to inspect. Position will be
reported in detector pixels rather than claiming a physical distance that the
current normalized model does not define.

The centroid will be calculated inside a fixed, symmetric detector window
around the center of the FFT image. This represents a finite detector and
prevents far-away FFT boundaries from distorting the measurement. The chosen
tilt range must keep the beam safely inside that window.

### Noise model

In a later milestone, zero-mean Gaussian noise will be added to the measured
centroid position. The initial model will therefore represent uncertainty in
the final position measurement, not photon-by-photon or camera-pixel noise.
This is a deliberate simplification and will be stated in the documentation.
A fixed random seed will make repeated experiments reproducible.

### Feedback model

A proportional controller will adjust the applied correction tilt using the
measured position error:

```text
tilt_correction_next = tilt_correction - gain * measured_position
```

The exact gain units will follow the Day One calibration between tilt waves
and detector pixels. The controller is intentionally simple: no PID control,
deformable-mirror model, machine learning, or adaptive estimator is planned.

### Measurements

The optical study will report:

- beam bias before correction;
- beam bias after correction;
- steady-state RMS positioning error;
- settling time;
- a clear comparison across controller gain and measurement-noise level.

Settling time will mean the first step after which the true position stays
inside a stated tolerance for the rest of the simulation. RMS error will be
calculated over a stated steady-state portion of the run. The final tolerance
and time-window values will be chosen and documented when the controller is
introduced, rather than being hidden constants.

### Optical milestones

#### Day One: noise-free measurement baseline

- Add a small script for horizontal beam-position measurement.
- Reuse the existing circular aperture, tilted field, and FFT functions.
- Measure a centered beam and several positive and negative tilts.
- Plot tilt in waves against measured centroid displacement in pixels.
- Fit a simple calibration line and report its slope.
- Add focused tests for centroid calculation, symmetry, direction, and input
  validation.
- Add a short README note and one understandable result figure.

Day One will not include measurement noise or feedback control. Its purpose is
to establish that the sensor responds predictably before the controller uses
that sensor.

#### Day Two: noisy detector measurements

- Add Gaussian centroid-measurement noise.
- Repeat measurements to show their distribution.
- Compare several noise levels with a fixed random seed.

#### Day Three: proportional feedback

- Add the one-dimensional feedback loop.
- Show position versus correction step before and after alignment.
- Verify that a reasonable gain reduces the initial error.

#### Day Four: gain and noise study

- Sweep a small set of gains and noise levels.
- Calculate RMS positioning error and settling time.
- Show stable, slow, and oscillating examples without overcomplicating them.

#### Day Five: validation and explanation

- Finish the result plots and README explanation.
- Check units, assumptions, reproducibility, and edge cases.
- Summarize what the simple controller can and cannot demonstrate.

These are work sessions rather than fixed calendar dates. A milestone can take
more than one day if the results need correction or explanation.

## Case Study B: Robotic Arm Trajectory Tracking

The robotics study will begin only after the optical case is understandable.
It will reuse the existing two-link forward and inverse kinematics functions.
The arm will follow a short reachable path while the model gradually adds:

1. a sequence of ideal inverse-kinematics targets;
2. joint-speed limits;
3. noisy position or joint-angle measurements;
4. simple proportional tracking correction;
5. comparisons of end-effector RMS error, maximum joint speed, and settling
   behavior.

The robotics case will receive its own detailed implementation plan when that
stage begins. Collision avoidance, dynamics, motor torque, three-dimensional
motion, and advanced trajectory optimization are outside the current scope.

## Validation Strategy

The studies will use small tests that express physical expectations:

- zero optical tilt produces a centered centroid;
- equal positive and negative tilts produce opposite displacements;
- a larger moderate tilt produces a larger displacement;
- a known synthetic intensity array produces the expected centroid;
- invalid or empty intensity data is rejected clearly;
- fixed random seeds reproduce noisy measurements;
- stable feedback reduces error in chosen test cases;
- decreasing or increasing gain changes convergence in an explainable way;
- later robotic inverse solutions still return to their requested targets.

Plots will support the numerical checks, not replace them.

## Repository Structure

The project will extend the current folders instead of creating a new umbrella
package:

```text
05_Optics/
  beam_alignment.py                 # begins on Day One
  README.md

04_Robotics_Simulator/
  ...                               # extended in the later robotics phase

tests/
  test_active_optical_alignment.py

assets/
  beam_tilt_calibration.png         # Day One result
```

Names may receive small adjustments during the implementation plan if an
existing naming convention makes another choice clearer.

## Dependencies and Style

Day One will use the repository's existing NumPy and Matplotlib dependencies.
No new dependency is required. Functions will remain short, variable names
will describe physical quantities, and comments will explain the model rather
than ordinary Python syntax.

The documentation will use cautious wording such as "conceptually related to"
when mentioning research directions. It will not claim laboratory-grade
fidelity, research experience, or a direct reproduction of Caltech work.

## Research Context

This learning direction is motivated by publicly described work in high-
contrast imaging, wavefront sensing and control, closed-loop optics, and the
sense-think-act structure of robotics. The project itself remains an
introductory numerical model.

Official background pages:

- Caltech Exoplanet Technology Laboratory:
  https://etlab.astro.caltech.edu/
- Dimitri Mawet research profile:
  https://etlab.caltech.edu/et-lab-people/dimitri-mawet
- Caltech Robotics Minor:
  https://mce.caltech.edu/academics/ugrad/robotics_minor
- Caltech Robotics courses:
  https://robot.caltech.edu/courses

## Completion Boundary

The umbrella project is complete when both case studies can run from the
repository root, produce understandable plots, report their stated metrics,
pass focused tests, and explain their limitations. Each daily commit should
contain one coherent learning step and remain readable on its own.
