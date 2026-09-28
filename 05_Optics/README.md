# Introductory Fourier-Optics Study

This folder is a small computational-optics study built as part of my Engineering Physics learning portfolio. The goal was to understand how an aperture and simple wavefront errors affect a far-field diffraction pattern, then check that the numerical result is stable when the grid is refined.

It is a learning project, not a model of NIF or a complete laser system.

## Main Question

How do aperture shape, defocus, and wavefront tilt change the far-field intensity pattern of coherent light?

The numerical model follows this sequence:

```text
aperture field -> phase error -> 2D FFT -> |amplitude|^2 -> intensity
```

For a circular aperture of radius `a`, the field is `1` inside the aperture and `0` outside it. Two simple phase models are used:

```text
defocus phase = 2 * pi * defocus_waves * (radius / a)^2
tilt phase    = 2 * pi * tilt_waves * x / (2 * a)
```

The calculations use normalized coordinates, so the plots show spatial-frequency samples rather than physical detector distances or angles.

## Study Sequence

| File | Question | Main output |
| --- | --- | --- |
| `fourier_optics.py` | What reusable calculations are needed? | Coordinate grids, aperture fields, phase errors, and FFT intensity |
| `diffraction_study.py` | What does ideal circular-aperture diffraction look like? | Two-dimensional pattern and center cross-section |
| `defocus_study.py` | How does one defocus value change the pattern? | Ideal and defocused patterns on the same intensity scale |
| `defocus_sweep.py` | How quickly does peak intensity fall as defocus grows? | Relative peak intensity from `0.0` to `1.0` wave |
| `tilt_study.py` | Does every phase error blur the pattern? | Beam-pointing shift caused by a linear phase ramp |
| `grid_convergence_study.py` | Is the reported defocus result dependent on grid size? | Peak intensity across five numerical resolutions |

## Key Results

| Experiment | Result |
| --- | --- |
| Ideal circular aperture | Bright central diffraction feature with weaker surrounding rings |
| `0.5` waves of defocus | Peak intensity falls to about `0.405` of the ideal peak |
| `1.0` wave of defocus | Peak intensity falls to about `0.049` of the ideal peak |
| `2.0` waves of tilt | Peak moves by `6` simulation pixels while retaining about `0.979` relative peak intensity |
| Grid refinement | The `0.5`-wave result changes by only `0.000084` from `257 × 257` to `513 × 513` |

These results show that defocus and tilt have different signatures. Defocus spreads light and lowers the peak, while tilt mainly shifts the location of the pattern.

## Run the Studies

Run the scripts from the repository root so the figures are saved in `assets/`:

```bash
python3 05_Optics/diffraction_study.py
python3 05_Optics/defocus_study.py
python3 05_Optics/defocus_sweep.py
python3 05_Optics/tilt_study.py
python3 05_Optics/grid_convergence_study.py
```

Run the automated tests with:

```bash
python3 -m unittest tests.test_fourier_optics -v
```

## What the Tests Check

The tests verify several physical and numerical expectations:

- the aperture and ideal diffraction pattern are centered and symmetric;
- a larger aperture produces a narrower central diffraction feature;
- zero defocus and zero tilt recover the original aperture field;
- phase errors preserve the aperture amplitude;
- defocus lowers the far-field peak;
- positive and negative tilt move the peak in opposite directions;
- finer grids produce a more stable defocus result;
- each plotting function can write to a requested output directory.

## Limitations

- The model uses scalar Fraunhofer diffraction.
- Coordinates and spatial-frequency axes are normalized.
- The source is treated as ideal, coherent, and monochromatic.
- Defocus and tilt are simplified phase functions rather than measured optical surfaces.
- The model does not include lenses, propagation distance, polarization, detector response, or a feedback-control system.

The most important lesson from this project was not only how to generate a diffraction plot, but how to compare cases fairly, vary one parameter at a time, test expected behavior, and check numerical convergence.
