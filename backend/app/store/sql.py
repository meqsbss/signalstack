from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models import (
    Briefing,
    ChangeEvent,
    Competitor,
    RevenueContext,
    Snapshot,
)
from app.orm_models import (
    BriefingRow,
    ChangeEventRow,
    CompetitorRow,
    RevenueContextRow,
    SnapshotRow,
)


class SqlStore:
    def __init__(self, session: Session) -> None:
        self.s = session

    def reset(self) -> None:
        for row in (SnapshotRow, ChangeEventRow, BriefingRow, RevenueContextRow, CompetitorRow):
            self.s.execute(delete(row))
        self.s.commit()

    # Competitors
    def add_competitor(self, c: Competitor) -> Competitor:
        self.s.add(CompetitorRow(**c.model_dump()))
        self.s.commit()
        return c

    def get_competitor(self, cid: str) -> Competitor | None:
        row = self.s.get(CompetitorRow, cid)
        if not row:
            return None
        return Competitor(
            id=row.id,
            name=row.name,
            domain=row.domain,
            trustmrr_slug=row.trustmrr_slug,
            created_at=row.created_at,
            last_refreshed_at=row.last_refreshed_at,
        )

    def list_competitors(self) -> list[Competitor]:
        rows = self.s.execute(select(CompetitorRow).order_by(CompetitorRow.name)).scalars()
        return [
            Competitor(
                id=r.id,
                name=r.name,
                domain=r.domain,
                trustmrr_slug=r.trustmrr_slug,
                created_at=r.created_at,
                last_refreshed_at=r.last_refreshed_at,
            )
            for r in rows
        ]

    def delete_competitor(self, cid: str) -> bool:
        row = self.s.get(CompetitorRow, cid)
        if not row:
            return False
        self.s.execute(delete(SnapshotRow).where(SnapshotRow.competitor_id == cid))
        self.s.execute(delete(ChangeEventRow).where(ChangeEventRow.competitor_id == cid))
        self.s.execute(delete(RevenueContextRow).where(RevenueContextRow.competitor_id == cid))
        self.s.delete(row)
        self.s.commit()
        return True

    def update_competitor(self, c: Competitor) -> None:
        row = self.s.get(CompetitorRow, c.id)
        if row:
            row.last_refreshed_at = c.last_refreshed_at
            self.s.commit()

    # Snapshots
    def latest_snapshot(self, cid: str, source_type: str) -> Snapshot | None:
        row = self.s.execute(
            select(SnapshotRow)
            .where(SnapshotRow.competitor_id == cid, SnapshotRow.source_type == source_type)
            .order_by(SnapshotRow.fetched_at.desc())
            .limit(1)
        ).scalar_one_or_none()
        if not row:
            return None
        return Snapshot(
            id=row.id,
            competitor_id=row.competitor_id,
            source_type=row.source_type,
            content_hash=row.content_hash,
            raw_text=row.raw_text,
            fetched_at=row.fetched_at,
        )

    def add_snapshot(self, s: Snapshot) -> None:
        self.s.add(SnapshotRow(**s.model_dump()))
        self.s.commit()

    # Events
    def add_event(self, e: ChangeEvent) -> None:
        self.s.add(ChangeEventRow(**e.model_dump()))
        self.s.commit()

    def list_events(self, cid: str) -> list[ChangeEvent]:
        rows = self.s.execute(
            select(ChangeEventRow)
            .where(ChangeEventRow.competitor_id == cid)
            .order_by(ChangeEventRow.detected_at.desc())
        ).scalars()
        return [self._event_from_row(r) for r in rows]

    def all_events(self) -> list[ChangeEvent]:
        rows = self.s.execute(select(ChangeEventRow)).scalars()
        return [self._event_from_row(r) for r in rows]

    def acknowledge_event(self, event_id: str) -> ChangeEvent | None:
        row = self.s.get(ChangeEventRow, event_id)
        if not row:
            return None
        row.acknowledged = True
        self.s.commit()
        return self._event_from_row(row)

    @staticmethod
    def _event_from_row(r: ChangeEventRow) -> ChangeEvent:
        return ChangeEvent(
            id=r.id,
            competitor_id=r.competitor_id,
            competitor_name=r.competitor_name,
            source_type=r.source_type,
            diff_summary=r.diff_summary,
            diff_full=r.diff_full,
            severity=r.severity,
            detected_at=r.detected_at,
            acknowledged=r.acknowledged,
        )

    # Revenue
    def get_revenue(self, cid: str) -> RevenueContext | None:
        row = self.s.get(RevenueContextRow, cid)
        if not row:
            return None
        return RevenueContext(
            competitor_id=row.competitor_id,
            mrr=row.mrr,
            growth_30d=row.growth_30d,
            verified_at=row.verified_at,
            source=row.source,
        )

    def set_revenue(self, r: RevenueContext) -> None:
        existing = self.s.get(RevenueContextRow, r.competitor_id)
        if existing:
            existing.mrr = r.mrr
            existing.growth_30d = r.growth_30d
            existing.verified_at = r.verified_at
        else:
            self.s.add(RevenueContextRow(**r.model_dump()))
        self.s.commit()

    # Briefings
    def add_briefing(self, b: Briefing) -> None:
        self.s.add(
            BriefingRow(
                id=b.id,
                week_start=b.week_start,
                summary_text=b.summary_text,
                top_event_ids=[e.id for e in b.top_events],
                created_at=b.created_at,
            )
        )
        self.s.commit()

    def latest_briefing(self) -> Briefing | None:
        row = self.s.execute(
            select(BriefingRow).order_by(BriefingRow.created_at.desc()).limit(1)
        ).scalar_one_or_none()
        if not row:
            return None
        events = []
        for eid in row.top_event_ids:
            e = self.s.get(ChangeEventRow, eid)
            if e:
                events.append(self._event_from_row(e))
        return Briefing(
            id=row.id,
            week_start=row.week_start,
            summary_text=row.summary_text,
            top_events=events,
            created_at=row.created_at,
        )