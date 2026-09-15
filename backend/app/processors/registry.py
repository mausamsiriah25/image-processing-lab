"""Central practical registry.

Maps a practical id to its processor function and processing metadata.
The API layer only ever does `REGISTRY[id]` lookups — it never branches on
practical id itself. Adding a practical means adding one entry here plus its
processor module and content JSON.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np

from . import (
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
from .base import ProcessingResult

ProcessorFn = Callable[[dict[str, np.ndarray], dict], ProcessingResult]


@dataclass(frozen=True)
class PracticalDefinition:
    id: str
    processor: ProcessorFn
    requires_image: bool = True
    multi_image: bool = False
    image_roles: tuple[str, ...] = ("image",)
    supports_report: bool = True


REGISTRY: dict[str, PracticalDefinition] = {
    "practical-01": PracticalDefinition(
        id="practical-01", processor=practical01.process, requires_image=False, image_roles=()
    ),
    "practical-02": PracticalDefinition(
        id="practical-02", processor=practical02.process, image_roles=("image", "image2")
    ),
    "practical-03": PracticalDefinition(id="practical-03", processor=practical03.process),
    "practical-04": PracticalDefinition(id="practical-04", processor=practical04.process),
    "practical-05": PracticalDefinition(id="practical-05", processor=practical05.process),
    "practical-06": PracticalDefinition(id="practical-06", processor=practical06.process),
    "practical-07": PracticalDefinition(id="practical-07", processor=practical07.process),
    "practical-08": PracticalDefinition(id="practical-08", processor=practical08.process),
    "practical-09": PracticalDefinition(
        id="practical-09",
        processor=practical09.process,
        multi_image=True,
        image_roles=("template", "target"),
    ),
    "postlab-02": PracticalDefinition(id="postlab-02", processor=postlab02.process),
    "postlab-03": PracticalDefinition(id="postlab-03", processor=postlab03.process),
}


def get_definition(practical_id: str) -> PracticalDefinition | None:
    return REGISTRY.get(practical_id)


def all_ids() -> list[str]:
    return list(REGISTRY.keys())
