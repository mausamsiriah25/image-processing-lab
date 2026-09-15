"""Practical 01 (Prelab) — Python & IDE Setup for Image Processing.

This practical is informational only: it introduces Python, IDE/editor
options, and the libraries used throughout the course. There is no image
transformation to run, so `process()` does not accept an uploaded image —
it simply reports which of the required libraries are importable in this
environment, which is itself a faithful "environment setup check" in the
spirit of the practical.
"""
from __future__ import annotations

from .base import ProcessingResult, table_output, timed


def _check_library(name: str) -> dict[str, str]:
    try:
        module = __import__(name)
        version = getattr(module, "__version__", "unknown")
        return {"library": name, "status": "installed", "version": str(version)}
    except ImportError:
        return {"library": name, "status": "not installed", "version": "-"}


def process(images: dict, params: dict) -> ProcessingResult:
    with timed() as t:
        libraries = ["numpy", "pandas", "sklearn", "matplotlib", "cv2"]
        rows = [_check_library(lib) for lib in libraries]

    return ProcessingResult(
        success=True,
        processing_time=t.elapsed,
        outputs=[
            table_output(
                "Environment Check",
                rows,
                caption="Required libraries for this course and their availability.",
            )
        ],
        metadata={"note": "Practical 01 is a setup/prelab practical; no image processing is performed."},
    )
