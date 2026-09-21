"""Compare ideal and defocused circular-aperture diffraction patterns."""

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
    create_defocused_field,
)


OUTPUT_PATH = "assets/defocus_aberration_comparison.png"


def save_defocus_comparison(
    ideal_intensity: np.ndarray,
    defocused_intensity: np.ndarray,
    defocus_waves: float,
    output_path: str = OUTPUT_PATH,
) -> None:
    """Save ideal and defocused patterns using the same intensity scale."""
    ideal_array = np.asarray(ideal_intensity)
    defocused_array = np.asarray(defocused_intensity)
    if ideal_array.ndim != 2 or ideal_array.shape != defocused_array.shape:
        raise ValueError("Intensity arrays must be matching 2D arrays.")
    if not np.all(np.isfinite(ideal_array)) or not np.all(
        np.isfinite(defocused_array)
    ):
        raise ValueError("Intensity values must be finite.")

    center = ideal_array.shape[0] // 2
    pixel_offsets = np.arange(ideal_array.shape[1]) - ideal_array.shape[1] // 2
    log_floor = 1e-6

    figure, axes = plt.subplots(1, 3, figsize=(14, 4.5), layout="constrained")
    image_options = {
        "cmap": "inferno",
        "origin": "lower",
        "vmin": -6,
        "vmax": 0,
    }

    ideal_image = axes[0].imshow(
        np.log10(ideal_array + log_floor),
        **image_options,
    )
    axes[0].set_title("Ideal Circular Aperture")
    axes[0].set_xlabel("Spatial-frequency sample")
    axes[0].set_ylabel("Spatial-frequency sample")

    axes[1].imshow(
        np.log10(defocused_array + log_floor),
        **image_options,
    )
    axes[1].set_title(f"Defocused ({defocus_waves:.1f} waves)")
    axes[1].set_xlabel("Spatial-frequency sample")
    axes[1].set_ylabel("Spatial-frequency sample")
    figure.colorbar(
        ideal_image,
        ax=axes[:2],
        label="log10 intensity relative to ideal peak",
        location="bottom",
        shrink=0.75,
        pad=0.08,
    )

    axes[2].plot(
        pixel_offsets,
        ideal_array[center],
        label="Ideal",
        color="#2563eb",
    )
    axes[2].plot(
        pixel_offsets,
        defocused_array[center],
        label="Defocused",
        color="#dc2626",
    )
    axes[2].set_title("Center Intensity Cross-Section")
    axes[2].set_xlabel("Spatial-frequency pixel offset")
    axes[2].set_ylabel("Intensity relative to ideal peak")
    axes[2].set_xlim(-30, 30)
    axes[2].set_ylim(bottom=0)
    axes[2].grid(alpha=0.3)
    axes[2].legend()

    figure.suptitle("Effect of Defocus on a Diffraction Pattern")
    output_directory = os.path.dirname(output_path)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)
    figure.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    grid_size = 257
    physical_size = 2.0
    aperture_radius = 0.35
    defocus_waves = 0.5

    x_grid, y_grid = create_coordinate_grid(grid_size, physical_size)
    aperture = create_circular_aperture(x_grid, y_grid, aperture_radius)
    defocused_field = create_defocused_field(
        aperture,
        x_grid,
        y_grid,
        aperture_radius,
        defocus_waves,
    )

    ideal_intensity = calculate_far_field_intensity(aperture, normalize=False)
    defocused_intensity = calculate_far_field_intensity(
        defocused_field,
        normalize=False,
    )
    ideal_peak = np.max(ideal_intensity)
    ideal_intensity /= ideal_peak
    defocused_intensity /= ideal_peak

    save_defocus_comparison(
        ideal_intensity,
        defocused_intensity,
        defocus_waves,
    )

    print("--- Defocus Aberration Study ---")
    print(f"Defocus: {defocus_waves:.1f} waves at the aperture edge")
    print(f"Ideal peak relative intensity: {np.max(ideal_intensity):.3f}")
    print(f"Defocused peak relative intensity: {np.max(defocused_intensity):.3f}")
    print("Model: quadratic phase error across a circular aperture")
    print(f"Plot saved to {OUTPUT_PATH}")
