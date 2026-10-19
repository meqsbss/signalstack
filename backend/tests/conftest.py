import os

os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base
from app.main import app
from app.services.fetcher import FakeFetcher
from app.store import set_store
from app.store.sql import SqlStore


@pytest.fixture(autouse=True)
def fresh_store():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    set_store(SqlStore(Session()))
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def fake_fetcher():
    f = FakeFetcher({})
    app.state.fetcher = f
    return f