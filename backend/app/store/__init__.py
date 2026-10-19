from __future__ import annotations

from app.db import SessionLocal
from app.store.sql import SqlStore

_store: SqlStore | None = None


def get_store() -> SqlStore:
    global _store
    if _store is None:
        _store = SqlStore(SessionLocal())
    return _store


def set_store(store: SqlStore) -> None:
    global _store
    _store = store