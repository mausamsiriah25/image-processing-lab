"""Pydantic models for report generation requests."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class StudentInfo(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    rollNumber: str = Field(default="", max_length=60)
    usn: str = Field(default="", max_length=60)
    semester: str = Field(default="", max_length=30)
    section: str = Field(default="", max_length=30)
    date: str = Field(default="", max_length=30)


class ReportRequest(BaseModel):
    studentInfo: StudentInfo
    result: dict[str, Any]  # the last ProcessingResponse payload, as returned by /process
    inputImages: dict[str, str] = {}  # role -> base64 data URL, e.g. {"image": "data:..."}
