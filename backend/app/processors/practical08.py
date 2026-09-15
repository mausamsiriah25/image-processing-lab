"""Practical 08 — Morphological Operations."""
from __future__ import annotations

import cv2
import numpy as np

from .base import Output, ProcessingError, ProcessingResult, image_output, table_output, timed

SHAPES = {
    "rect": cv2.MORPH_RECT,
    "ellipse": cv2.MORPH_ELLIPSE,
    "cross": cv2.MORPH_CROSS,
}


def _binarize(img: np.ndarray, threshold: int) -> np.ndarray:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return binary


def _white_area(binary: np.ndarray) -> int:
    return int(np.count_nonzero(binary == 255))


def process(images: dict[str, np.ndarray], params: dict) -> ProcessingResult:
    if "image" not in images:
        raise ProcessingError("An input image is required for this practical.")
    img = images["image"]

    binarize_threshold = int(params.get("binarizeThreshold", 127))
    kernel_size = int(params.get("kernelSize", 5))
    kernel_shape = params.get("kernelShape", "rect")
    iterations = int(params.get("iterations", 1))

    if kernel_shape not in SHAPES:
        raise ProcessingError(f"Unsupported kernel shape '{kernel_shape}'.")

    with timed() as t:
        binary = _binarize(img, binarize_threshold)
        kernel = cv2.getStructuringElement(SHAPES[kernel_shape], (kernel_size, kernel_size))

        erosion = cv2.erode(binary, kernel, iterations=iterations)
        dilation = cv2.dilate(binary, kernel, iterations=iterations)
        opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=iterations)
        closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=iterations)

        outputs: list[Output] = [
            image_output("Original Image", img, "practical-08-original.png"),
            image_output("Binary Image", binary, "practical-08-binary.png"),
            image_output("Erosion", erosion, "practical-08-erosion.png"),
            image_output("Dilation", dilation, "practical-08-dilation.png"),
            image_output("Opening", opening, "practical-08-opening.png"),
            image_output("Closing", closing, "practical-08-closing.png"),
            table_output(
                "Object Area Analysis (white-pixel count)",
                [
                    {"operation": "Binary (original)", "areaPixels": _white_area(binary)},
                    {"operation": "Erosion", "areaPixels": _white_area(erosion)},
                    {"operation": "Dilation", "areaPixels": _white_area(dilation)},
                    {"operation": "Opening", "areaPixels": _white_area(opening)},
                    {"operation": "Closing", "areaPixels": _white_area(closing)},
                ],
                caption="Effect of each morphological operation on object (foreground) area.",
            ),
        ]

    return ProcessingResult(
        success=True,
        processing_time=t.elapsed,
        outputs=outputs,
        metadata={"kernelSize": kernel_size, "kernelShape": kernel_shape, "iterations": iterations},
    )
