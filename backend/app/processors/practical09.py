"""Practical 09 — Object Detection Using Correlation Principle (Template Matching)."""
from __future__ import annotations

import cv2
import numpy as np

from .base import Output, ProcessingError, ProcessingResult, image_output, value_output, timed


def process(images: dict[str, np.ndarray], params: dict) -> ProcessingResult:
    if "template" not in images or "target" not in images:
        raise ProcessingError("This practical requires two images: a template and a target image.")

    template = images["template"]
    target = images["target"]
    match_threshold = float(params.get("matchThreshold", 0.8))

    th, tw = template.shape[:2]
    gh, gw = target.shape[:2]
    if th > gh or tw > gw:
        raise ProcessingError("The template image must be smaller than the target image.")

    with timed() as t:
        result_map = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result_map)

        annotated = target.copy()
        detected = max_val >= match_threshold
        if detected:
            top_left = max_loc
            bottom_right = (top_left[0] + tw, top_left[1] + th)
            cv2.rectangle(annotated, top_left, bottom_right, (0, 255, 0), 3)

        outputs: list[Output] = [
            image_output("Template Image", template, "practical-09-template.png"),
            image_output("Target Image", target, "practical-09-target.png"),
            image_output(
                "Detected Object" if detected else "Detection Result (below threshold)",
                annotated,
                "practical-09-detected.png",
            ),
            value_output("Match Score", round(float(max_val), 4)),
            value_output("Object Detected", bool(detected)),
        ]

    return ProcessingResult(
        success=True,
        processing_time=t.elapsed,
        outputs=outputs,
        metadata={"matchThreshold": match_threshold, "matchMethod": "TM_CCOEFF_NORMED"},
        warnings=[] if detected else ["Match score is below the detection threshold."],
    )
