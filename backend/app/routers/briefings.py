from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models import Briefing, ErrorResponse
from app.services.briefing import build_briefing
from app.store import get_store

router = APIRouter(prefix="/briefings", tags=["briefings"])


@router.post("/generate", response_model=Briefing)
async def generate() -> Briefing:
    store = get_store()
    briefing = build_briefing(store.all_events())
    store.add_briefing(briefing)
    return briefing


@router.get("/latest", response_model=Briefing, responses={404: {"model": ErrorResponse}})
async def latest() -> Briefing:
    b = get_store().latest_briefing()
    if not b:
        raise HTTPException(status_code=404, detail="No briefing yet")
    return b