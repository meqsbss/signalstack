from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from app.models import Briefing, ErrorResponse
from app.observability import record_briefing
from app.services.briefing import build_briefing
from app.store import get_store

router = APIRouter(prefix="/briefings", tags=["briefings"])
logger = logging.getLogger(__name__)


@router.post("/generate", response_model=Briefing)
async def generate() -> Briefing:
    store = get_store()
    briefing = build_briefing(store.all_events())
    store.add_briefing(briefing)
    record_briefing()
    logger.info("Weekly briefing generated")
    return briefing


@router.get("/latest", response_model=Briefing, responses={404: {"model": ErrorResponse}})
async def latest() -> Briefing:
    briefing = get_store().latest_briefing()
    if not briefing:
        raise HTTPException(status_code=404, detail="No briefing yet")
    return briefing
