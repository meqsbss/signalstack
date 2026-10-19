from __future__ import annotations

import hashlib

from fastapi import APIRouter, HTTPException, Request

from app.models import (
    ChangeEvent,
    Competitor,
    CompetitorCreate,
    ErrorResponse,
    RevenueContext,
    Snapshot,
    now_iso,
)
from app.services import trustmrr
from app.services.diff import classify_severity, summarize, unified_diff
from app.services.fetcher import Fetcher, urls_for
from app.store import get_store

router = APIRouter(prefix="/competitors", tags=["competitors"])


@router.post(
    "",
    response_model=Competitor,
    status_code=201,
    responses={422: {"model": ErrorResponse}},
)
async def create_competitor(body: CompetitorCreate) -> Competitor:
    if "." not in body.domain:
        raise HTTPException(status_code=422, detail="Invalid domain")
    c = Competitor(name=body.name, domain=body.domain, trustmrr_slug=body.trustmrr_slug)
    get_store().add_competitor(c)
    return c


@router.get("", response_model=list[Competitor])
async def list_competitors() -> list[Competitor]:
    return get_store().list_competitors()


@router.get(
    "/{competitor_id}",
    response_model=Competitor,
    responses={404: {"model": ErrorResponse}},
)
async def get_competitor(competitor_id: str) -> Competitor:
    c = get_store().get_competitor(competitor_id)
    if not c:
        raise HTTPException(status_code=404, detail="Competitor not found")
    return c


@router.delete(
    "/{competitor_id}",
    status_code=204,
    responses={404: {"model": ErrorResponse}},
)
async def delete_competitor(competitor_id: str) -> None:
    if not get_store().delete_competitor(competitor_id):
        raise HTTPException(status_code=404, detail="Competitor not found")


@router.post(
    "/{competitor_id}/refresh",
    response_model=list[ChangeEvent],
    responses={404: {"model": ErrorResponse}},
)
async def refresh_competitor(competitor_id: str, request: Request) -> list[ChangeEvent]:
    store = get_store()
    competitor = store.get_competitor(competitor_id)
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")

    fetcher: Fetcher = request.app.state.fetcher
    urls = urls_for(competitor.domain)

    new_events: list[ChangeEvent] = []
    for source_type, url in urls.items():
        try:
            text = await fetcher.fetch(url)
        except FileNotFoundError:
            continue
        except TimeoutError:
            raise HTTPException(status_code=502, detail=f"Timeout fetching {source_type}")

        h = hashlib.sha256(text.encode()).hexdigest()
        prev = store.latest_snapshot(competitor_id, source_type)
        store.add_snapshot(
            Snapshot(
                competitor_id=competitor_id,
                source_type=source_type,
                content_hash=h,
                raw_text=text,
            )
        )
        if prev and prev.content_hash != h:
            diff = unified_diff(prev.raw_text, text)
            event = ChangeEvent(
                competitor_id=competitor_id,
                competitor_name=competitor.name,
                source_type=source_type,
                diff_summary=summarize(diff),
                diff_full=diff,
                severity=classify_severity(diff),
            )
            store.add_event(event)
            new_events.append(event)

    competitor.last_refreshed_at = now_iso()
    store.update_competitor(competitor)
    return new_events


@router.get(
    "/{competitor_id}/revenue",
    response_model=RevenueContext | None,
    responses={404: {"model": ErrorResponse}},
)
async def get_revenue(competitor_id: str) -> RevenueContext | None:
    store = get_store()
    competitor = store.get_competitor(competitor_id)
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")

    cached = store.get_revenue(competitor_id)
    if cached and not trustmrr.is_stale(cached.verified_at):
        return cached

    if not competitor.trustmrr_slug:
        return cached

    fresh = await trustmrr.fetch_revenue(competitor.trustmrr_slug)
    if fresh:
        fresh.competitor_id = competitor_id
        store.set_revenue(fresh)
        return fresh
    return cached