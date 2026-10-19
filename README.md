# SignalStack

Competitive intelligence dashboard for indie SaaS founders. Tracks
competitors' pricing, changelog, and homepage pages, detects meaningful
changes, enriches them with TrustMRR revenue data, and produces a weekly
briefing.

## Stack

- **Frontend:** React 18 + TypeScript + Vite, React Router, Vitest
- **Backend:** FastAPI + SQLAlchemy + SQLite, pytest
- **Contract:** `openapi.yaml` (generated from FastAPI)

## Run locally

### Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8091