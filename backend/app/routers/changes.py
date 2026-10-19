from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models import ChangeEvent, ErrorResponse
from app.store.memory import get_store

router = APIRouter(prefix="/competitors", tags=["changes"])


@router.get("/{competitor_id}/changes", response_model=list[ChangeEvent])
async def list_changes(competitor_id: str) -> list[ChangeEvent]:
    store = get_store()
    if competitor_id not in store.competitors:
        raise HTTPException(status_code=404, detail="Competitor not found")
    return sorted(
        [e for e in store.events if e.competitor_id == competitor_id],
        key=lambda e: e.detected_at,
        reverse=True,
    )


@router.post(
    "/{competitor_id}/changes/{event_id}/acknowledge",
    response_model=ChangeEvent,
    responses={404: {"model": ErrorResponse}},
)
async def acknowledge(competitor_id: str, event_id: str) -> ChangeEvent:
    store = get_store()
    for e in store.events:
        if e.id == event_id and e.competitor_id == competitor_id:
            e.acknowledged = True
            return e
    raise HTTPException(status_code=404, detail="Event not found")