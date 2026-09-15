"""Practical 02 — Image I/O, Colour Conversion, Arithmetic & Bitwise Ops."""
from __future__ import annotations

import cv2
import numpy as np

from .base import Output, ProcessingError, ProcessingResult, image_output, timed

TWO_IMAGE_OPS = {"add", "addWeighted", "subtract", "bitwise_and", "bitwise_or", "bitwise_xor"}


def _match_size(img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
    """Resize img2 to img1's size if they differ, so arithmetic/bitwise ops are valid."""
    if img1.shape[:2] != img2.shape[:2]:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    return img2


def process(images: dict[str, np.ndarray], params: dict) -> ProcessingResult:
    if "image" not in images:
        raise ProcessingError("An input image is required for this practical.")

    operation = params.get("operation", "grayscale")
    img = images["image"]

    with timed() as t:
        outputs: list[Output] = [image_output("Original Image", img, "practical-02-original.png")]

        if operation == "grayscale":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            outputs.append(image_output("Grayscale Image", gray, "practical-02-grayscale.png"))

        elif operation == "bgr2rgb":
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            outputs.append(image_output("RGB (channel-swapped) Image", rgb, "practical-02-rgb.png"))

        elif operation in TWO_IMAGE_OPS:
            if "image2" not in images:
                raise ProcessingError(f"Operation '{operation}' requires a second image.")
            img2 = _match_size(img, images["image2"])
            outputs.append(image_output("Second Image", img2, "practical-02-image2.png"))

            if operation == "add":
                result = cv2.add(img, img2)
                label = "Added Image (cv2.add)"
            elif operation == "addWeighted":
                w1 = float(params.get("weight1", 0.5))
                w2 = float(params.get("weight2", 0.5))
                gamma = float(params.get("gamma", 0))
                result = cv2.addWeighted(img, w1, img2, w2, gamma)
                label = "Weighted Sum (cv2.addWeighted)"
            elif operation == "subtract":
                result = cv2.subtract(img, img2)
                label = "Subtracted Image (cv2.subtract)"
            elif operation == "bitwise_and":
                result = cv2.bitwise_and(img, img2)
                label = "Bitwise AND"
            elif operation == "bitwise_or":
                result = cv2.bitwise_or(img, img2)
                label = "Bitwise OR"
            elif operation == "bitwise_xor":
                result = cv2.bitwise_xor(img, img2)
                label = "Bitwise XOR"
            else:
                raise ProcessingError(f"Unsupported operation '{operation}'.")

            outputs.append(image_output(label, result, "practical-02-result.png"))

        elif operation == "bitwise_not":
            result = cv2.bitwise_not(img)
            outputs.append(image_output("Bitwise NOT (Inverted)", result, "practical-02-not.png"))

        else:
            raise ProcessingError(f"Unsupported operation '{operation}'.")

    return ProcessingResult(
        success=True,
        processing_time=t.elapsed,
        outputs=outputs,
        metadata={"operation": operation},
    )
