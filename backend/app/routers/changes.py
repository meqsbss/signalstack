from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models import ChangeEvent, ErrorResponse
from app.store import get_store

router = APIRouter(prefix="/competitors", tags=["changes"])
events_router = APIRouter(prefix="/events", tags=["events"])


@router.get(
    "/{competitor_id}/changes",
    response_model=list[ChangeEvent],
    responses={404: {"model": ErrorResponse}},
)
async def list_changes(competitor_id: str) -> list[ChangeEvent]:
    store = get_store()
    if not store.get_competitor(competitor_id):
        raise HTTPException(status_code=404, detail="Competitor not found")
    return store.list_events(competitor_id)


@router.post(
    "/{competitor_id}/changes/{event_id}/acknowledge",
    response_model=ChangeEvent,
    responses={404: {"model": ErrorResponse}},
)
async def acknowledge(competitor_id: str, event_id: str) -> ChangeEvent:
    e = get_store().acknowledge_event(event_id)
    if not e or e.competitor_id != competitor_id:
        raise HTTPException(status_code=404, detail="Event not found")
    return e


@events_router.post(
    "/{event_id}/acknowledge",
    response_model=ChangeEvent,
    responses={404: {"model": ErrorResponse}},
)
async def acknowledge_direct(event_id: str) -> ChangeEvent:
    e = get_store().acknowledge_event(event_id)
    if not e:
        raise HTTPException(status_code=404, detail="Event not found")
    return e