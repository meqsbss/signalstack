from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id() -> str:
    return str(uuid4())


SourceType = Literal["pricing", "changelog", "homepage"]
Severity = Literal["low", "medium", "high"]


class Competitor(BaseModel):
    id: str = Field(default_factory=new_id)
    name: str
    domain: str
    trustmrr_slug: str | None = None
    created_at: str = Field(default_factory=now_iso)
    last_refreshed_at: str | None = None


class CompetitorCreate(BaseModel):
    name: str
    domain: str
    trustmrr_slug: str | None = None


class Snapshot(BaseModel):
    id: str = Field(default_factory=new_id)
    competitor_id: str
    source_type: SourceType
    content_hash: str
    raw_text: str
    fetched_at: str = Field(default_factory=now_iso)


class ChangeEvent(BaseModel):
    id: str = Field(default_factory=new_id)
    competitor_id: str
    competitor_name: str
    source_type: SourceType
    diff_summary: str
    diff_full: str
    severity: Severity
    detected_at: str = Field(default_factory=now_iso)
    acknowledged: bool = False


class RevenueContext(BaseModel):
    competitor_id: str
    mrr: int
    growth_30d: float
    verified_at: str
    source: Literal["trustmrr"] = "trustmrr"


class Briefing(BaseModel):
    id: str = Field(default_factory=new_id)
    week_start: str
    summary_text: str
    top_events: list[ChangeEvent]
    created_at: str = Field(default_factory=now_iso)


class ErrorResponse(BaseModel):
    detail: str