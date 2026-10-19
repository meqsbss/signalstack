from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta, timezone

import httpx

from app.models import RevenueContext, now_iso

log = logging.getLogger(__name__)

BASE_URL = os.getenv("TRUSTMRR_BASE_URL", "https://trustmrr.com/api")
API_KEY = os.getenv("TRUSTMRR_API_KEY", "")


async def fetch_revenue(slug: str) -> RevenueContext | None:
    if not API_KEY or not slug:
        return None
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.get(
                f"{BASE_URL}/startups/{slug}",
                headers={"Authorization": f"Bearer {API_KEY}"},
            )
            if res.status_code >= 400:
                log.warning("TrustMRR returned %s for %s", res.status_code, slug)
                return None
            data = res.json()
            return RevenueContext(
                competitor_id="",  # filled by caller
                mrr=int(data.get("mrr", 0)),
                growth_30d=float(data.get("growth_30d", 0)),
                verified_at=now_iso(),
                source="trustmrr",
            )
    except Exception as e:
        log.warning("TrustMRR fetch failed for %s: %s", slug, e)
        return None


def is_stale(verified_at: str) -> bool:
    try:
        ts = datetime.fromisoformat(verified_at)
    except ValueError:
        return True
    return datetime.now(timezone.utc) - ts > timedelta(hours=24)