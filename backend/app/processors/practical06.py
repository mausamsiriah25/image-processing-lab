"""Practical 06 — Image Restoration (Inpainting & Denoising).

V1 scope (see docs/ARCHITECTURE.md §6): automatic damage-mask detection only.
Manual mask drawing is a documented future extension, not implemented here.
"""
from __future__ import annotations

import cv2
import numpy as np

from .base import Output, ProcessingError, ProcessingResult, image_output, timed

MODES = ["inpaint_telea", "inpaint_ns", "denoise_gaussian", "denoise_median", "denoise_nlm"]


def _auto_mask(img: np.ndarray, threshold: int) -> np.ndarray:
    """Detect 'damaged' pixels as near-black regions, matching the source
    code's approach of thresholding near-black pixels to build a mask."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img
    _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
    return mask


def process(images: dict[str, np.ndarray], params: dict) -> ProcessingResult:
    if "image" not in images:
        raise ProcessingError("An input image is required for this practical.")
    img = images["image"]
    mode = params.get("mode", "inpaint_telea")

    with timed() as t:
        outputs: list[Output] = [image_output("Original / Damaged Image", img, "practical-06-original.png")]

        if mode in ("inpaint_telea", "inpaint_ns"):
            mask_threshold = int(params.get("maskThreshold", 30))
            radius = int(params.get("inpaintRadius", 3))
            mask = _auto_mask(img, mask_threshold)
            outputs.append(image_output("Detected Damage Mask", mask, "practical-06-mask.png"))

            algo = cv2.INPAINT_TELEA if mode == "inpaint_telea" else cv2.INPAINT_NS
            restored = cv2.inpaint(img, mask, radius, algo)
            label = "Restored Image (Telea)" if mode == "inpaint_telea" else "Restored Image (Navier-Stokes)"
            outputs.append(image_output(label, restored, f"practical-06-{mode}.png"))

        elif mode == "denoise_gaussian":
            k = int(params.get("kernelSize", 5))
            k = k if k % 2 == 1 else k + 1
            result = cv2.GaussianBlur(img, (k, k), 0)
            outputs.append(image_output("Denoised (Gaussian Blur)", result, "practical-06-denoise-gaussian.png"))

        elif mode == "denoise_median":
            k = int(params.get("kernelSize", 5))
            k = k if k % 2 == 1 else k + 1
            result = cv2.medianBlur(img, k)
            outputs.append(image_output("Denoised (Median Filter)", result, "practical-06-denoise-median.png"))

        elif mode == "denoise_nlm":
            h = float(params.get("nlmH", 10))
            template_window = int(params.get("templateWindowSize", 7))
            search_window = int(params.get("searchWindowSize", 21))
            if img.ndim == 3:
                result = cv2.fastNlMeansDenoisingColored(img, None, h, h, template_window, search_window)
            else:
                result = cv2.fastNlMeansDenoising(img, None, h, template_window, search_window)
            outputs.append(image_output("Denoised (Non-local Means)", result, "practical-06-denoise-nlm.png"))

        else:
            raise ProcessingError(f"Unsupported mode '{mode}'.")

    return ProcessingResult(success=True, processing_time=t.elapsed, outputs=outputs, metadata={"mode": mode})
