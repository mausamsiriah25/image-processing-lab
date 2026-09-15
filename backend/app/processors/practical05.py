"""Practical 05 — Spatial Domain Filters."""
from __future__ import annotations

import cv2
import numpy as np

from .base import Output, ProcessingError, ProcessingResult, image_output, timed

FILTERS = ["averaging", "box", "gaussian", "median", "bilateral"]


def _apply(name: str, img: np.ndarray, params: dict) -> np.ndarray:
    k = int(params.get("kernelSize", 5))
    k = k if k % 2 == 1 else k + 1
    k = max(k, 3)

    if name == "averaging":
        return cv2.blur(img, (k, k))
    if name == "box":
        return cv2.boxFilter(img, -1, (k, k))
    if name == "gaussian":
        sigma = float(params.get("sigmaX", 0))
        return cv2.GaussianBlur(img, (k, k), sigma)
    if name == "median":
        return cv2.medianBlur(img, k)
    if name == "bilateral":
        diameter = int(params.get("diameter", 9))
        sigma_color = float(params.get("sigmaColor", 75))
        sigma_space = float(params.get("sigmaSpace", 75))
        return cv2.bilateralFilter(img, diameter, sigma_color, sigma_space)
    raise ProcessingError(f"Unsupported filter '{name}'.")


LABELS = {
    "averaging": "Averaging Filter",
    "box": "Box Filter",
    "gaussian": "Gaussian Filter",
    "median": "Median Filter",
    "bilateral": "Bilateral Filter",
}


def process(images: dict[str, np.ndarray], params: dict) -> ProcessingResult:
    if "image" not in images:
        raise ProcessingError("An input image is required for this practical.")
    img = images["image"]
    selected = params.get("filter", "gaussian")

    with timed() as t:
        outputs: list[Output] = [image_output("Original Image", img, "practical-05-original.png")]

        if selected == "all":
            for name in FILTERS:
                result = _apply(name, img, params)
                outputs.append(image_output(LABELS[name], result, f"practical-05-{name}.png"))
        else:
            if selected not in FILTERS:
                raise ProcessingError(f"Unsupported filter '{selected}'.")
            result = _apply(selected, img, params)
            outputs.append(image_output(LABELS[selected], result, f"practical-05-{selected}.png"))

    return ProcessingResult(success=True, processing_time=t.elapsed, outputs=outputs, metadata={"filter": selected})
