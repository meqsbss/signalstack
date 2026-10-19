from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.models import Briefing, ChangeEvent, now_iso

SEVERITY_RANK = {"high": 0, "medium": 1, "low": 2}


def build_briefing(events: list[ChangeEvent]) -> Briefing:
    cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
    candidates = [e for e in events if not e.acknowledged and e.detected_at >= cutoff]
    candidates.sort(key=lambda e: (SEVERITY_RANK[e.severity], _neg(e.detected_at)))
    top = candidates[:10]

    now = datetime.now(timezone.utc)
    week_start = (now - timedelta(days=now.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    if not top:
        summary = "No changes this week."
    else:
        competitors = len({e.competitor_id for e in top})
        summary = (
            f"Week of {week_start.date().isoformat()}: "
            f"{len(top)} changes across {competitors} competitors. "
            f"Top: {top[0].diff_summary}"
        )

    return Briefing(
        week_start=week_start.isoformat(),
        summary_text=summary,
        top_events=top,
        created_at=now_iso(),
    )


def _neg(iso: str) -> str:
    return "".join(chr(255 - ord(c)) for c in iso)