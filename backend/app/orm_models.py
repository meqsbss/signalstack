from __future__ import annotations

from sqlalchemy import JSON, Boolean, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class CompetitorRow(Base):
    __tablename__ = "competitors"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    domain: Mapped[str] = mapped_column(String, nullable=False)
    trustmrr_slug: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[str] = mapped_column(String, nullable=False)
    last_refreshed_at: Mapped[str | None] = mapped_column(String, nullable=True)


class SnapshotRow(Base):
    __tablename__ = "snapshots"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    competitor_id: Mapped[str] = mapped_column(String, index=True)
    source_type: Mapped[str] = mapped_column(String, nullable=False)
    content_hash: Mapped[str] = mapped_column(String, nullable=False)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    fetched_at: Mapped[str] = mapped_column(String, nullable=False)


class ChangeEventRow(Base):
    __tablename__ = "change_events"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    competitor_id: Mapped[str] = mapped_column(String, index=True)
    competitor_name: Mapped[str] = mapped_column(String, nullable=False)
    source_type: Mapped[str] = mapped_column(String, nullable=False)
    diff_summary: Mapped[str] = mapped_column(Text, nullable=False)
    diff_full: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String, nullable=False)
    detected_at: Mapped[str] = mapped_column(String, nullable=False)
    acknowledged: Mapped[bool] = mapped_column(Boolean, default=False)


class BriefingRow(Base):
    __tablename__ = "briefings"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    week_start: Mapped[str] = mapped_column(String, nullable=False)
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    top_event_ids: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[str] = mapped_column(String, nullable=False)


class RevenueContextRow(Base):
    __tablename__ = "revenue_contexts"
    competitor_id: Mapped[str] = mapped_column(String, primary_key=True)
    mrr: Mapped[int] = mapped_column(Integer, nullable=False)
    growth_30d: Mapped[float] = mapped_column(Float, nullable=False)
    verified_at: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)