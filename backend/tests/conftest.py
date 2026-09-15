import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@pytest.fixture
def sample_image() -> np.ndarray:
    rng = np.random.default_rng(42)
    img = (rng.random((64, 64, 3)) * 255).astype(np.uint8)
    return img


@pytest.fixture
def sample_image_2() -> np.ndarray:
    rng = np.random.default_rng(7)
    img = (rng.random((64, 64, 3)) * 255).astype(np.uint8)
    return img
