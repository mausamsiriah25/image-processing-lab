"""Shared processor interface and result types.

Every practical processor implements:

    def process(images: dict[str, np.ndarray], params: dict) -> ProcessingResult

`images` is keyed by role ("image", "template", "target", ...) so that
multi-image practicals (e.g. practical-09) fit the same contract as
single-image ones.
"""
from __future__ import annotations

import base64
import time
from dataclasses import dataclass, field
from typing import Any, Literal

import cv2
import numpy as np

OutputType = Literal["image", "chart", "value", "table"]


@dataclass
class Output:
    name: str
    type: OutputType
    data: Any
    caption: str | None = None
    filename: str | None = None


@dataclass
class ProcessingResult:
    success: bool
    processing_time: float
    outputs: list[Output] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "processingTime": round(self.processing_time, 4),
            "outputs": [
                {
                    "name": o.name,
                    "type": o.type,
                    "data": o.data,
                    "caption": o.caption,
                    "filename": o.filename,
                }
                for o in self.outputs
            ],
            "metadata": self.metadata,
            "warnings": self.warnings,
            "error": self.error,
        }


class ProcessingError(Exception):
    """Raised by a processor for an expected, user-facing failure
    (bad parameters, image too small for an operation, etc.)."""


def image_to_data_url(image: np.ndarray, ext: str = ".png") -> str:
    """Encode a BGR or grayscale numpy image as a base64 data URL."""
    if image is None:
        raise ProcessingError("Cannot encode an empty image.")
    ok, buffer = cv2.imencode(ext, image)
    if not ok:
        raise ProcessingError("Failed to encode output image.")
    mime = "image/png" if ext == ".png" else "image/jpeg"
    b64 = base64.b64encode(buffer.tobytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def figure_to_data_url(fig) -> str:
    """Encode a Matplotlib figure as a base64 PNG data URL."""
    import io

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=110)
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("ascii")
    import matplotlib.pyplot as plt

    plt.close(fig)
    return f"data:image/png;base64,{b64}"


def image_output(name: str, image: np.ndarray, filename: str, caption: str | None = None, ext: str = ".png") -> Output:
    return Output(name=name, type="image", data=image_to_data_url(image, ext), caption=caption, filename=filename)


def chart_output(name: str, fig, filename: str, caption: str | None = None) -> Output:
    return Output(name=name, type="chart", data=figure_to_data_url(fig), caption=caption, filename=filename)


def value_output(name: str, value: Any, caption: str | None = None) -> Output:
    return Output(name=name, type="value", data=value, caption=caption)


def table_output(name: str, rows: list[dict[str, Any]], caption: str | None = None) -> Output:
    return Output(name=name, type="table", data=rows, caption=caption)


class timed:
    """Context manager that measures elapsed wall-clock time in seconds."""

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, *exc):
        self.elapsed = time.perf_counter() - self._start
