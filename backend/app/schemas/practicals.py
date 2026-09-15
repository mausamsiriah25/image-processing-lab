"""Pydantic response models for practical content endpoints."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel


class ParameterSpec(BaseModel):
    key: str
    label: str
    type: Literal["slider", "number", "select", "radio", "checkbox"]
    min: float | None = None
    max: float | None = None
    step: float | None = None
    default: Any = None
    options: list[dict[str, str]] | None = None


class PracticalSummary(BaseModel):
    id: str
    number: int
    type: Literal["practical", "postlab"]
    title: str
    category: str
    aim: str
    requiresImage: bool
    multiImage: bool = False


class PracticalDetail(PracticalSummary):
    objectives: list[str]
    theory: str
    algorithm: list[str]
    referenceCode: str
    syntax: list[str] = []
    parameters: list[ParameterSpec] = []
    expectedOutputs: list[str] = []
    observation: str
    conclusion: str
    postLab: list[str] = []


class PracticalListResponse(BaseModel):
    practicals: list[PracticalSummary]
    total: int
