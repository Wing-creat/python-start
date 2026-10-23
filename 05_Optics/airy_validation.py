"""Compare circular-aperture FFT intensity with the analytical Airy pattern."""

import os
from pathlib import Path

import numpy as np
from scipy.special import j1

from fourier_optics import (
    calculate_far_field_intensity,
    create_circular_aperture,
    create_coordinate_grid,
)


def airy_intensity(frequencies, aperture_radius):
    """Return peak-normalized intensity; frequency is cycles per coordinate unit."""
    frequencies = np.asarray(frequencies, dtype=float)
    if not np.all(np.isfinite(frequencies)):
        raise ValueError("Frequencies must be finite.")
    if not np.isfinite(aperture_radius) or aperture_radius <= 0:
        raise ValueError("Aperture radius must be positive and finite.")
    u = 2 * np.pi * aperture_radius * frequencies
    amplitude = np.ones_like(u)
    np.divide(2 * j1(u), u, out=amplitude, where=u != 0)
    return amplitude ** 2


def compare_airy(grid_size, physical_size=2.0, aperture_radius=0.35):
    """Return a center slice and theory on common frequencies from -6 to 6.

    Zero-padding fixes frequency spacing across grids; it does not improve
    the sampled aperture. Errors describe normalized shape, not absolute power.
    """
    x, y = create_coordinate_grid(grid_size, physical_size)
    if not 0 < aperture_radius < physical_size / 2:
        raise ValueError("The aperture must fit inside the coordinate grid.")
    spacing = physical_size / (grid_size - 1)
    if 1 / (2 * spacing) <= 6:
        raise ValueError("Grid is too coarse for the comparison frequency range.")
    aperture = create_circular_aperture(x, y, aperture_radius)

    # M * spacing = 4 * physical_size for every N: identical FFT frequencies.
    padded_size = 4 * (grid_size - 1)
    before = (padded_size - grid_size) // 2
    after = padded_size - grid_size - before
    padded = np.pad(aperture, ((before, after), (before, after)))
    intensity = calculate_far_field_intensity(padded)
    frequencies = np.fft.fftshift(np.fft.fftfreq(padded_size, d=spacing))
    selected = np.abs(frequencies) <= 6
    frequencies = frequencies[selected]
    numerical = intensity[padded_size // 2, selected]
    theory = airy_intensity(frequencies, aperture_radius)
    return frequencies, numerical, theory


def main():
    os.environ.setdefault("MPLCONFIGDIR", ".matplotlib_cache")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sizes = [33, 65, 129, 257, 513]
    rms_errors = []
    max_errors = []
    print("Airy validation: L=2.0, radius=0.35, frequency range [-6, 6]")
    print("Errors use peak-normalized intensity at 97 shared frequency samples.")
    print("Grid       RMSE          Max absolute error")
    figure, axes = plt.subplots(1, 2, figsize=(10, 4.5), layout="constrained")
    for size in sizes:
        frequencies, numerical, theory = compare_airy(size)
        error = numerical - theory
        rms_errors.append(float(np.sqrt(np.mean(error ** 2))))
        max_errors.append(float(np.max(np.abs(error))))
        print(f"{size:4d}    {rms_errors[-1]:.6e}    {max_errors[-1]:.6e}")
        if size in (33, 513):
            for axis in axes:
                axis.plot(frequencies, numerical, ".", markersize=3, label=f"FFT N={size}")

    smooth_frequencies = np.linspace(-6, 6, 1001)
    for axis in axes:
        axis.plot(smooth_frequencies, airy_intensity(smooth_frequencies, 0.35),
                  color="black", linewidth=1, label="Airy theory")
        axis.set_xlabel("Spatial frequency (cycles / coordinate unit)")
        axis.set_ylabel("Peak-normalized intensity")
        axis.grid(alpha=0.25)
        axis.legend()
    axes[0].set_title("Central peak")
    axes[1].set_title("Weak rings (log view)")
    axes[1].set_yscale("log")
    axes[1].set_ylim(1e-6, 1.2)
    Path("assets").mkdir(exist_ok=True)
    figure.savefig("assets/airy_comparison.png", dpi=160)
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(7, 4.5), layout="constrained")
    axis.loglog(sizes, rms_errors, "o-", label="RMSE")
    axis.loglog(sizes, max_errors, "s-", label="Maximum absolute error")
    axis.set(xlabel="Aperture grid samples per side (N)",
             ylabel="Normalized-intensity error", title="FFT Error Against Airy Theory")
    axis.set_xticks(sizes, labels=[str(size) for size in sizes])
    axis.grid(alpha=0.25)
    axis.legend()
    figure.savefig("assets/airy_grid_error.png", dpi=160)
    plt.close(figure)
    print("Plots saved to assets/airy_comparison.png and assets/airy_grid_error.png")


if __name__ == "__main__":
    main()
