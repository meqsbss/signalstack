from __future__ import annotations

import pytest

from app.models import RevenueContext
from app.services import trustmrr


@pytest.mark.asyncio
async def test_fetch_revenue_without_key(monkeypatch):
    monkeypatch.setattr(trustmrr, "API_KEY", "")
    assert await trustmrr.fetch_revenue("acme") is None


@pytest.mark.asyncio
async def test_fetch_revenue_http_error(monkeypatch):
    monkeypatch.setattr(trustmrr, "API_KEY", "test")

    class FakeClient:
        def __init__(self, *a, **kw): ...
        async def __aenter__(self): return self
        async def __aexit__(self, *a): ...
        async def get(self, *a, **kw):
            class R:
                status_code = 500
                def json(self): return {}
            return R()

    monkeypatch.setattr(trustmrr.httpx, "AsyncClient", FakeClient)
    assert await trustmrr.fetch_revenue("acme") is None


def test_is_stale():
    assert trustmrr.is_stale("2020-01-01T00:00:00+00:00") is True
    from app.models import now_iso
    assert trustmrr.is_stale(now_iso()) is False