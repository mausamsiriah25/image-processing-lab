import cv2
import numpy as np
import pytest

from app.processors.base import ProcessingError
from app.services.image_io import decode_upload


def _encode_png(img: np.ndarray) -> bytes:
    ok, buf = cv2.imencode(".png", img)
    assert ok
    return buf.tobytes()


def test_decode_valid_image():
    img = (np.random.rand(20, 20, 3) * 255).astype(np.uint8)
    raw = _encode_png(img)
    decoded = decode_upload(raw, "image/png")
    assert decoded.shape[:2] == (20, 20)


def test_decode_rejects_empty_bytes():
    with pytest.raises(ProcessingError):
        decode_upload(b"", "image/png")


def test_decode_rejects_garbage_bytes():
    with pytest.raises(ProcessingError):
        decode_upload(b"not an image", "image/png")


def test_decode_rejects_disallowed_mime_type():
    img = (np.random.rand(20, 20, 3) * 255).astype(np.uint8)
    raw = _encode_png(img)
    with pytest.raises(ProcessingError):
        decode_upload(raw, "application/pdf")
