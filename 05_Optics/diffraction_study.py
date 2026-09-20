"""Run and visualize a simple circular-aperture diffraction study."""

import os

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from fourier_optics import (
    calculate_far_field_intensity,
    create_circular_aperture,
    create_coordinate_grid,
)


OUTPUT_PATH = "assets/circular_aperture_diffraction.png"


def save_diffraction_plot(
    aperture: np.ndarray,
    intensity: np.ndarray,
    output_path: str = OUTPUT_PATH,
) -> None:
    """Save the aperture, diffraction pattern, and center cross-section."""
    if aperture.shape != intensity.shape or aperture.ndim != 2:
        raise ValueError("Aperture and intensity must be matching 2D arrays.")

    center = intensity.shape[0] // 2
    pixel_offsets = np.arange(intensity.shape[1]) - intensity.shape[1] // 2

    figure, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    axes[0].imshow(aperture, cmap="gray", origin="lower")
    axes[0].set_title("Circular Aperture")
    axes[0].set_xlabel("Grid sample")
    axes[0].set_ylabel("Grid sample")

    image = axes[1].imshow(
        np.log10(intensity + 1e-6),
        cmap="inferno",
        origin="lower",
    )
    axes[1].set_title("Far-Field Intensity (log scale)")
    axes[1].set_xlabel("Spatial-frequency sample")
    axes[1].set_ylabel("Spatial-frequency sample")
    figure.colorbar(image, ax=axes[1], label="log10 normalized intensity")

    axes[2].plot(pixel_offsets, intensity[center], color="#2563eb")
    axes[2].set_title("Center Intensity Cross-Section")
    axes[2].set_xlabel("Spatial-frequency pixel offset")
    axes[2].set_ylabel("Normalized intensity")
    axes[2].set_xlim(-30, 30)
    axes[2].grid(alpha=0.3)

    figure.suptitle("Fraunhofer Diffraction from a Circular Aperture")
    figure.tight_layout()
    output_directory = os.path.dirname(output_path)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)
    figure.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    grid_size = 257
    physical_size = 2.0
    aperture_radius = 0.35

    x_grid, y_grid = create_coordinate_grid(grid_size, physical_size)
    aperture = create_circular_aperture(x_grid, y_grid, aperture_radius)
    intensity = calculate_far_field_intensity(aperture)
    save_diffraction_plot(aperture, intensity)

    print("--- Circular-Aperture Diffraction Study ---")
    print(f"Grid size: {grid_size} x {grid_size}")
    print(f"Normalized aperture radius: {aperture_radius}")
    print(f"Peak normalized intensity: {np.max(intensity):.2f}")
    print("Model: scalar Fraunhofer diffraction with normalized coordinates")
    print(f"Plot saved to {OUTPUT_PATH}")
