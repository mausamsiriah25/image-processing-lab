"""Practical 04 — Spatial Domain Image Enhancement."""
from __future__ import annotations

import cv2
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .base import Output, ProcessingError, ProcessingResult, chart_output, image_output, timed

THRESH_TYPES = {
    "binary": cv2.THRESH_BINARY,
    "binary_inv": cv2.THRESH_BINARY_INV,
    "trunc": cv2.THRESH_TRUNC,
    "tozero": cv2.THRESH_TOZERO,
    "tozero_inv": cv2.THRESH_TOZERO_INV,
}


def _to_gray(img: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img


def process(images: dict[str, np.ndarray], params: dict) -> ProcessingResult:
    if "image" not in images:
        raise ProcessingError("An input image is required for this practical.")
    img = images["image"]
    operation = params.get("operation", "negative")

    with timed() as t:
        outputs: list[Output] = [image_output("Original Image", img, "practical-04-original.png")]

        if operation == "negative":
            outputs.append(image_output("Negative Image", 255 - img, "practical-04-negative.png"))

        elif operation == "brightness_contrast":
            alpha = float(params.get("alpha", 1.2))
            beta = float(params.get("beta", 30))
            result = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
            outputs.append(image_output("Brightness/Contrast Adjusted", result, "practical-04-bc.png"))

        elif operation == "brightness_contrast_scaling":
            alpha = float(params.get("alpha", 1.2))
            beta = float(params.get("beta", 30))
            result = np.clip(img.astype(np.float32) * alpha + beta, 0, 255).astype(np.uint8)
            outputs.append(image_output("Brightness/Contrast (manual scaling)", result, "practical-04-bc-scaled.png"))

        elif operation == "sharpen":
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            result = cv2.filter2D(img, -1, kernel)
            outputs.append(image_output("Sharpened Image", result, "practical-04-sharpen.png"))

        elif operation == "laplacian":
            gray = _to_gray(img)
            lap = cv2.Laplacian(gray, cv2.CV_64F)
            lap_abs = cv2.convertScaleAbs(lap)
            sharpened = cv2.convertScaleAbs(gray.astype(np.float32) - lap)
            outputs.append(image_output("Laplacian Edge Response", lap_abs, "practical-04-laplacian.png"))
            outputs.append(image_output("Laplacian-Sharpened Image", sharpened, "practical-04-laplacian-sharp.png"))

        elif operation == "median":
            k = int(params.get("medianKernel", 5))
            k = k if k % 2 == 1 else k + 1
            result = cv2.medianBlur(img, k)
            outputs.append(image_output("Median Filtered Image", result, "practical-04-median.png"))

        elif operation == "histogram_equalization":
            gray = _to_gray(img)
            equalized = cv2.equalizeHist(gray)
            outputs.append(image_output("Grayscale Image", gray, "practical-04-gray.png"))
            outputs.append(image_output("Histogram Equalized Image", equalized, "practical-04-equalized.png"))

            fig, axes = plt.subplots(1, 2, figsize=(8, 3))
            axes[0].hist(gray.ravel(), bins=256, range=(0, 255), color="#4f46e5")
            axes[0].set_title("Original Histogram")
            axes[1].hist(equalized.ravel(), bins=256, range=(0, 255), color="#06b6d4")
            axes[1].set_title("Equalized Histogram")
            for ax in axes:
                ax.set_xlabel("Pixel Intensity")
                ax.set_ylabel("Frequency")
            fig.tight_layout()
            outputs.append(chart_output("Histogram Comparison", fig, "practical-04-histogram.png"))

        elif operation == "threshold":
            gray = _to_gray(img)
            value = int(params.get("thresholdValue", 120))
            thresh_type = params.get("thresholdType", "all")
            if thresh_type == "all":
                for name, cv_type in THRESH_TYPES.items():
                    _, result = cv2.threshold(gray, value, 255, cv_type)
                    outputs.append(image_output(f"Threshold: {name}", result, f"practical-04-threshold-{name}.png"))
            else:
                if thresh_type not in THRESH_TYPES:
                    raise ProcessingError(f"Unsupported threshold type '{thresh_type}'.")
                _, result = cv2.threshold(gray, value, 255, THRESH_TYPES[thresh_type])
                outputs.append(image_output(f"Threshold: {thresh_type}", result, f"practical-04-threshold-{thresh_type}.png"))

        else:
            raise ProcessingError(f"Unsupported operation '{operation}'.")

    return ProcessingResult(success=True, processing_time=t.elapsed, outputs=outputs, metadata={"operation": operation})
