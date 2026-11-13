"""Pydantic models for API requests and responses."""
from typing import Optional

from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    requirement: str = Field(..., min_length=10, max_length=2000)
    model: Optional[str] = None
    temperature: Optional[float] = Field(default=None, ge=0, le=1)


class StageResult(BaseModel):
    agent: str
    output: str
    seconds: float


class RunResponse(BaseModel):
    run_id: str
    created_at: str
    requirement: str
    stages: list[StageResult]
    final_code: str
    report: str
