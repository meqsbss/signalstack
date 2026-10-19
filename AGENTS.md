# SignalStack - Agent Instructions

## Project
SignalStack is a competitive intelligence dashboard for indie SaaS founders.
It tracks competitors' pricing/changelog pages, detects meaningful changes,
enriches them with TrustMRR revenue data, and produces a weekly briefing.

## Commands

### Backend (Python / FastAPI)
- `cd backend && uv sync` - install dependencies
- `cd backend && uv run uvicorn app.main:app --reload --port 8091` - run dev server
- `cd backend && uv run pytest` - run all tests
- `cd backend && uv run pytest tests/test_competitors.py` - one test file

### Frontend (React / TypeScript / Vite)
- `cd frontend && npm install` - install dependencies
- `cd frontend && npm run dev` - run dev server (default port 5173)
- `cd frontend && npm run test` - run tests
- `cd frontend && npm run build` - production build

## Rules
- Dependencies are added in `backend/pyproject.toml` or `frontend/package.json`.
  Do not add a new dependency without asking.
- Commit after every meaningful change.
- Every backend change must keep `openapi.yaml` in sync.
- Never use SQLite-specific SQL. Use SQLAlchemy ORM only (DB-agnostic).
- Never close a GitHub issue yourself unless you are the QA agent.

## Documents
- `_docs/plan.md` - full product specification
- `_docs/process.md` - how work is organized (PM -> Engineer -> QA)
- `_docs/task-template.md` - the four-section issue format
- `_docs/design-system.md` - UI tokens and component rules
- `_docs/testing-guidelines.md` - what to test and how
- `_docs/team/pm.md` - Product Manager agent role
- `_docs/team/software-engineer.md` - Engineer agent role
- `_docs/team/qa-engineer.md` - QA agent role

Before any UI work, read `_docs/design-system.md`.
Before writing tests, read `_docs/testing-guidelines.md`.