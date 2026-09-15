"""Loads structured practical content JSON files (single source of truth
for theory/aim/objectives/code, shared by the API and the report builder)."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from ..core.config import settings


class ContentNotFoundError(Exception):
    pass


@lru_cache(maxsize=1)
def _load_all() -> dict[str, dict]:
    content_dir = Path(settings.content_dir)
    content: dict[str, dict] = {}
    if not content_dir.exists():
        return content
    for path in sorted(content_dir.glob("*.json")):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            content[data["id"]] = data
    return content


def list_practicals() -> list[dict]:
    items = list(_load_all().values())
    return sorted(items, key=lambda p: (p.get("type") != "practical", p.get("number", 0)))


def get_practical(practical_id: str) -> dict:
    content = _load_all()
    if practical_id not in content:
        raise ContentNotFoundError(f"No content found for practical '{practical_id}'.")
    return content[practical_id]


def reload_cache() -> None:
    """Clears the in-memory content cache (useful for tests / hot content edits)."""
    _load_all.cache_clear()
