from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import init_db
from app.routers import briefings, changes, competitors
from app.services.fetcher import HttpFetcher

app = FastAPI(title="SignalStack API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.fetcher = HttpFetcher()

app.include_router(competitors.router)
app.include_router(changes.router)
app.include_router(changes.events_router)
app.include_router(briefings.router)


@app.on_event("startup")
async def on_startup() -> None:
    init_db()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}