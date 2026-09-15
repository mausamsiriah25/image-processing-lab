"""Post Lab 03 — Edge Detection: Canny vs Sobel vs Prewitt."""
from __future__ import annotations

import cv2
import numpy as np

from .base import Output, ProcessingError, ProcessingResult, image_output, timed

PREWITT_KX = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
PREWITT_KY = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)


def _to_gray(img: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img


def _canny(gray: np.ndarray, low: int, high: int, blur_kernel: int) -> np.ndarray:
    k = blur_kernel if blur_kernel % 2 == 1 else blur_kernel + 1
    blurred = cv2.GaussianBlur(gray, (k, k), 0)
    return cv2.Canny(blurred, low, high)


def _sobel(gray: np.ndarray) -> np.ndarray:
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = cv2.magnitude(gx, gy)
    return cv2.convertScaleAbs(magnitude)


def _prewitt(gray: np.ndarray) -> np.ndarray:
    gx = cv2.filter2D(gray.astype(np.float32), -1, PREWITT_KX)
    gy = cv2.filter2D(gray.astype(np.float32), -1, PREWITT_KY)
    magnitude = cv2.magnitude(gx, gy)
    return cv2.convertScaleAbs(magnitude)


def process(images: dict[str, np.ndarray], params: dict) -> ProcessingResult:
    if "image" not in images:
        raise ProcessingError("An input image is required for this practical.")
    img = images["image"]
    gray = _to_gray(img)

    canny_low = int(params.get("cannyLow", 100))
    canny_high = int(params.get("cannyHigh", 200))
    blur_kernel = int(params.get("gaussianKernel", 5))

    with timed() as t:
        canny = _canny(gray, canny_low, canny_high, blur_kernel)
        sobel = _sobel(gray)
        prewitt = _prewitt(gray)

        comparison = np.hstack(
            [
                cv2.resize(canny, (gray.shape[1], gray.shape[0])),
                cv2.resize(sobel, (gray.shape[1], gray.shape[0])),
                cv2.resize(prewitt, (gray.shape[1], gray.shape[0])),
            ]
        )

        outputs: list[Output] = [
            image_output("Grayscale Image", gray, "postlab-03-gray.png"),
            image_output("Canny Edge Map", canny, "postlab-03-canny.png"),
            image_output("Sobel Gradient Magnitude", sobel, "postlab-03-sobel.png"),
            image_output("Prewitt Gradient Magnitude", prewitt, "postlab-03-prewitt.png"),
            image_output(
                "Comparison (Canny | Sobel | Prewitt)",
                comparison,
                "postlab-03-comparison.png",
                caption="Left to right: Canny, Sobel, Prewitt.",
            ),
        ]

    return ProcessingResult(
        success=True,
        processing_time=t.elapsed,
        outputs=outputs,
        metadata={"cannyLow": canny_low, "cannyHigh": canny_high, "gaussianKernel": blur_kernel},
    )
