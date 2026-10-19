from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.fetcher import FakeFetcher
from app.store.memory import MemoryStore, set_store


@pytest.fixture(autouse=True)
def fresh_store():
    set_store(MemoryStore())
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def fake_fetcher():
    f = FakeFetcher({})
    app.state.fetcher = f
    return f