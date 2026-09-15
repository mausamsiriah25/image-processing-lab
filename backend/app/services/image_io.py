"""Safe image decoding / validation helpers.

Uploaded files are treated as untrusted input: validated for type, size, and
decoded dimensions before any processing touches them.
"""
from __future__ import annotations

import cv2
import numpy as np

from ..core.config import settings
from ..processors.base import ProcessingError


def decode_upload(raw_bytes: bytes, content_type: str | None) -> np.ndarray:
    if content_type is not None and content_type not in settings.allowed_image_types:
        raise ProcessingError(
            f"Unsupported file type '{content_type}'. Allowed types: JPG, JPEG, PNG, WEBP."
        )
    if len(raw_bytes) == 0:
        raise ProcessingError("Uploaded file is empty.")
    if len(raw_bytes) > settings.max_upload_size_bytes:
        max_mb = settings.max_upload_size_bytes / (1024 * 1024)
        raise ProcessingError(f"File exceeds the maximum allowed size of {max_mb:.0f} MB.")

    buffer = np.frombuffer(raw_bytes, dtype=np.uint8)
    image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
    if image is None:
        raise ProcessingError("The uploaded file could not be read as an image. It may be corrupted.")

    h, w = image.shape[:2]
    if h > settings.max_image_dimension or w > settings.max_image_dimension:
        raise ProcessingError(
            f"Image dimensions ({w}x{h}) exceed the maximum allowed "
            f"({settings.max_image_dimension}px per side)."
        )
    if h < 4 or w < 4:
        raise ProcessingError("Image is too small to process.")

    return image
