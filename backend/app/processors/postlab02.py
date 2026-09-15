"""Post Lab 02 — Colour Space Conversion."""
from __future__ import annotations

import cv2
import numpy as np

from .base import Output, ProcessingError, ProcessingResult, image_output, timed

SPACES = ["grayscale", "channels", "ycrcb", "hsv", "lab"]


def _apply(space: str, img: np.ndarray) -> list[Output]:
    if space == "grayscale":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return [image_output("Grayscale Image", gray, "postlab-02-grayscale.png")]

    if space == "channels":
        b, g, r = cv2.split(img)
        return [
            image_output("Blue Channel", b, "postlab-02-blue.png"),
            image_output("Green Channel", g, "postlab-02-green.png"),
            image_output("Red Channel", r, "postlab-02-red.png"),
        ]

    if space == "ycrcb":
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        return [image_output("YCrCb Image", ycrcb, "postlab-02-ycrcb.png")]

    if space == "hsv":
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        return [image_output("HSV Image", hsv, "postlab-02-hsv.png")]

    if space == "lab":
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
        return [image_output("Lab Image", lab, "postlab-02-lab.png")]

    raise ProcessingError(f"Unsupported colour space '{space}'.")


def process(images: dict[str, np.ndarray], params: dict) -> ProcessingResult:
    if "image" not in images:
        raise ProcessingError("An input image is required for this practical.")
    img = images["image"]
    target_space = params.get("targetSpace", "hsv")

    with timed() as t:
        outputs: list[Output] = [image_output("Original Image", img, "postlab-02-original.png")]
        if target_space == "all":
            for space in SPACES:
                outputs.extend(_apply(space, img))
        else:
            if target_space not in SPACES:
                raise ProcessingError(f"Unsupported colour space '{target_space}'.")
            outputs.extend(_apply(target_space, img))

    return ProcessingResult(success=True, processing_time=t.elapsed, outputs=outputs, metadata={"targetSpace": target_space})
