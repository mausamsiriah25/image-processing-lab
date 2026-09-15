"""Practical 03 — 2D Geometric Transformations."""
from __future__ import annotations

import cv2
import numpy as np

from .base import Output, ProcessingError, ProcessingResult, image_output, timed

ALL_OPS = [
    "translation",
    "reflection",
    "rotation",
    "shrink",
    "enlarge",
    "crop",
    "shear_x",
    "shear_y",
]


def _apply(op: str, img: np.ndarray, params: dict) -> np.ndarray:
    h, w = img.shape[:2]

    if op == "translation":
        tx = float(params.get("tx", 50))
        ty = float(params.get("ty", 50))
        M = np.float32([[1, 0, tx], [0, 1, ty]])
        return cv2.warpAffine(img, M, (w, h))

    if op == "reflection":
        return cv2.flip(img, 0)  # reflection along X-axis

    if op == "rotation":
        angle = float(params.get("angle", 45))
        center = (w / 2, h / 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(img, M, (w, h))

    if op == "shrink":
        scale = float(params.get("scale", 0.5))
        scale = min(max(scale, 0.05), 0.99)
        return cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    if op == "enlarge":
        scale = float(params.get("scale", 1.5))
        scale = max(scale, 1.01)
        return cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

    if op == "crop":
        x1 = int(params.get("x1", w * 0.1))
        y1 = int(params.get("y1", h * 0.1))
        x2 = int(params.get("x2", w * 0.9))
        y2 = int(params.get("y2", h * 0.9))
        x1, x2 = sorted((max(0, min(x1, w - 1)), max(0, min(x2, w))))
        y1, y2 = sorted((max(0, min(y1, h - 1)), max(0, min(y2, h))))
        if x2 - x1 < 2 or y2 - y1 < 2:
            raise ProcessingError("Crop region is too small.")
        return img[y1:y2, x1:x2]

    if op == "shear_x":
        factor = float(params.get("shearFactor", 0.2))
        M = np.float32([[1, factor, 0], [0, 1, 0]])
        return cv2.warpAffine(img, M, (int(w + factor * h), h))

    if op == "shear_y":
        factor = float(params.get("shearFactor", 0.2))
        M = np.float32([[1, 0, 0], [factor, 1, 0]])
        return cv2.warpAffine(img, M, (w, int(h + factor * w)))

    raise ProcessingError(f"Unsupported operation '{op}'.")


LABELS = {
    "translation": "Translated Image",
    "reflection": "Reflected Image (X-axis)",
    "rotation": "Rotated Image",
    "shrink": "Shrunk Image",
    "enlarge": "Enlarged Image",
    "crop": "Cropped Image",
    "shear_x": "Sheared Image (X-axis)",
    "shear_y": "Sheared Image (Y-axis)",
}


def process(images: dict[str, np.ndarray], params: dict) -> ProcessingResult:
    if "image" not in images:
        raise ProcessingError("An input image is required for this practical.")
    img = images["image"]
    operation = params.get("operation", "translation")

    with timed() as t:
        outputs: list[Output] = [image_output("Original Image", img, "practical-03-original.png")]

        if operation == "all":
            for op in ALL_OPS:
                result = _apply(op, img, params)
                outputs.append(image_output(LABELS[op], result, f"practical-03-{op}.png"))
        else:
            if operation not in ALL_OPS:
                raise ProcessingError(f"Unsupported operation '{operation}'.")
            result = _apply(operation, img, params)
            outputs.append(image_output(LABELS[operation], result, f"practical-03-{operation}.png"))

    return ProcessingResult(success=True, processing_time=t.elapsed, outputs=outputs, metadata={"operation": operation})
