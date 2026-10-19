from __future__ import annotations

from app.models import (
    Briefing,
    ChangeEvent,
    Competitor,
    RevenueContext,
    Snapshot,
)


class MemoryStore:
    def __init__(self) -> None:
        self.competitors: dict[str, Competitor] = {}
        self.snapshots: list[Snapshot] = []
        self.events: list[ChangeEvent] = []
        self.briefings: list[Briefing] = []
        self.revenue: dict[str, RevenueContext] = {}

    def reset(self) -> None:
        self.competitors.clear()
        self.snapshots.clear()
        self.events.clear()
        self.briefings.clear()
        self.revenue.clear()


_store: MemoryStore | None = None


def get_store() -> MemoryStore:
    global _store
    if _store is None:
        _store = MemoryStore()
    return _store


def set_store(store: MemoryStore) -> None:
    global _store
    _store = store