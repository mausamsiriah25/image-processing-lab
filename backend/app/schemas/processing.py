"""Pydantic request/response models for the processing endpoint."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel


class OutputSchema(BaseModel):
    name: str
    type: Literal["image", "chart", "value", "table"]
    data: Any
    caption: str | None = None
    filename: str | None = None


class ProcessingResponse(BaseModel):
    success: bool
    processingTime: float
    outputs: list[OutputSchema]
    metadata: dict[str, Any] = {}
    warnings: list[str] = []
    error: str | None = None


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail
