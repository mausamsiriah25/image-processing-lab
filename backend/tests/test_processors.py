"""Every processor: input -> processor -> expected ProcessingResult shape.

This is the minimum bar required by CLAUDE.md: every practical processor
must have a basic test confirming it returns a well-formed, successful
ProcessingResult for valid input.
"""
import cv2
import numpy as np
import pytest

from app.processors import (
    postlab02,
    postlab03,
    practical01,
    practical02,
    practical03,
    practical04,
    practical05,
    practical06,
    practical07,
    practical08,
    practical09,
)
from app.processors.base import ProcessingError


def _assert_valid_result(result):
    assert result.success is True
    assert result.processing_time >= 0
    assert len(result.outputs) >= 1
    for output in result.outputs:
        assert output.type in {"image", "chart", "value", "table"}
        assert output.data is not None


def test_practical01_no_image_needed():
    result = practical01.process({}, {})
    _assert_valid_result(result)
    assert result.outputs[0].type == "table"


@pytest.mark.parametrize(
    "operation", ["grayscale", "bgr2rgb", "bitwise_not"]
)
def test_practical02_single_image_ops(sample_image, operation):
    result = practical02.process({"image": sample_image}, {"operation": operation})
    _assert_valid_result(result)


@pytest.mark.parametrize(
    "operation", ["add", "addWeighted", "subtract", "bitwise_and", "bitwise_or", "bitwise_xor"]
)
def test_practical02_two_image_ops(sample_image, sample_image_2, operation):
    result = practical02.process({"image": sample_image, "image2": sample_image_2}, {"operation": operation})
    _assert_valid_result(result)


def test_practical02_missing_second_image_raises(sample_image):
    with pytest.raises(ProcessingError):
        practical02.process({"image": sample_image}, {"operation": "add"})


@pytest.mark.parametrize("operation", practical03.ALL_OPS + ["all"])
def test_practical03_all_transforms(sample_image, operation):
    result = practical03.process({"image": sample_image}, {"operation": operation})
    _assert_valid_result(result)


@pytest.mark.parametrize(
    "operation",
    [
        "negative",
        "brightness_contrast",
        "brightness_contrast_scaling",
        "sharpen",
        "laplacian",
        "median",
        "histogram_equalization",
        "threshold",
    ],
)
def test_practical04_all_operations(sample_image, operation):
    result = practical04.process({"image": sample_image}, {"operation": operation})
    _assert_valid_result(result)


def test_practical04_histogram_equalization_has_chart(sample_image):
    result = practical04.process({"image": sample_image}, {"operation": "histogram_equalization"})
    assert any(o.type == "chart" for o in result.outputs)


@pytest.mark.parametrize("filter_name", practical05.FILTERS + ["all"])
def test_practical05_filters(sample_image, filter_name):
    result = practical05.process({"image": sample_image}, {"filter": filter_name})
    _assert_valid_result(result)


@pytest.mark.parametrize("mode", practical06.MODES)
def test_practical06_restoration_modes(sample_image, mode):
    result = practical06.process({"image": sample_image}, {"mode": mode})
    _assert_valid_result(result)


@pytest.mark.parametrize("method", practical07.METHODS)
def test_practical07_compression_methods(sample_image, method):
    result = practical07.process({"image": sample_image}, {"method": method})
    _assert_valid_result(result)
    # Every method must report whether reconstruction is lossless.
    assert any("lossless" in (o.name or "").lower() or o.name == "PNG reconstruction is lossless" for o in result.outputs)


def test_practical08_morphology(sample_image):
    result = practical08.process({"image": sample_image}, {"kernelSize": 5, "iterations": 1})
    _assert_valid_result(result)
    assert any(o.type == "table" for o in result.outputs)


def test_practical09_object_detection():
    target = np.zeros((120, 120, 3), dtype=np.uint8)
    cv2.rectangle(target, (40, 40), (80, 80), (255, 255, 255), -1)
    template = target[40:80, 40:80].copy()
    result = practical09.process({"template": template, "target": target}, {"matchThreshold": 0.8})
    _assert_valid_result(result)
    match_score = next(o.data for o in result.outputs if o.name == "Match Score")
    assert match_score > 0.9


def test_practical09_requires_two_images(sample_image):
    with pytest.raises(ProcessingError):
        practical09.process({"template": sample_image}, {})


@pytest.mark.parametrize("space", postlab02.SPACES + ["all"])
def test_postlab02_colour_spaces(sample_image, space):
    result = postlab02.process({"image": sample_image}, {"targetSpace": space})
    _assert_valid_result(result)


def test_postlab03_edge_detection(sample_image):
    result = postlab03.process({"image": sample_image}, {})
    _assert_valid_result(result)
    names = {o.name for o in result.outputs}
    assert "Canny Edge Map" in names
    assert "Sobel Gradient Magnitude" in names
    assert "Prewitt Gradient Magnitude" in names


def test_missing_image_raises_for_image_practicals(sample_image):
    for module in (practical03, practical04, practical05, practical06, practical07, postlab02, postlab03):
        with pytest.raises(ProcessingError):
            module.process({}, {})
