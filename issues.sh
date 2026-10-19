#!/usr/bin/env bash
set -euo pipefail

# SignalStack MVP backlog. Creates 18 issues with the `mvp` label.
# Requires: gh auth login, run from repo root.

REPO="meqsbss/signalstack"

# Ensure the label exists (idempotent: ignore error if already present)
gh label create mvp --repo "$REPO" --color "0E8A16" --description "MVP scope" 2>/dev/null || true
gh label create post-mvp --repo "$REPO" --color "FBCA04" --description "Post-MVP scope" 2>/dev/null || true
gh label create user-test-bug --repo "$REPO" --color "D73A4A" --description "Bug found during manual testing" 2>/dev/null || true

create_issue() {
  local title="$1"
  local body="$2"
  gh issue create --repo "$REPO" --title "$title" --body "$body" --label mvp
}

# ---------------------------------------------------------------------------
# 1
create_issue "Scaffold frontend with Vite + React + TypeScript" "$(cat <<'EOF'
## Goal

A `frontend/` directory exists with a runnable Vite + React + TypeScript
app and a passing test, so that later issues can add UI without touching
tooling.

## Acceptance criteria

- [ ] `cd frontend && npm install && npm run dev` starts a dev server on port 5173
- [ ] `cd frontend && npm run build` exits 0
- [ ] `cd frontend && npm run test` runs vitest and passes with at least one trivial test
- [ ] `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/index.html` exist
- [ ] `frontend/src/styles/tokens.css` defines every CSS variable from `_docs/design-system.md`
- [ ] Inter and JetBrains Mono are loaded (via `@fontsource` packages or a Google Fonts link)
- [ ] `.gitignore` already excludes `node_modules/` and `dist/`

## Out of scope

- Any actual UI beyond a placeholder "SignalStack" heading
- Routing

## Constraints

- Vite, React 18, TypeScript strict mode
- No CSS framework (Tailwind etc.) — plain CSS modules or a single `global.css`
- Follow `_docs/design-system.md` tokens
EOF
)"

# ---------------------------------------------------------------------------
# 2
create_issue "Create SignalService interface and MockSignalService" "$(cat <<'EOF'
## Goal

All frontend data access goes through `frontend/src/services/SignalService.ts`.
A `MockSignalService` implements it with in-memory data so the whole app
runs without a backend.

## Acceptance criteria

- [ ] `SignalService.ts` exports an interface with methods:
      `listCompetitors`, `getCompetitor`, `addCompetitor`, `deleteCompetitor`,
      `refreshCompetitor`, `listChangeEvents`, `acknowledgeChangeEvent`,
      `getRevenueContext`, `getLatestBriefing`, `generateBriefing`
- [ ] `MockSignalService.ts` implements every method, uses 300ms artificial delay
- [ ] Mock data includes at least 3 competitors, each with 2+ change events and one with revenue data
- [ ] `MockSignalService.test.ts` covers every method (happy path)
- [ ] No component imports `MockSignalService` directly; they import the interface via a provider
- [ ] `frontend/src/services/provider.ts` exports `getSignalService()` that returns the mock in dev

## Out of scope

- HTTP implementation (issue #15)
- Error injection beyond a simple `throw new Error("...")` path

## Constraints

- TypeScript types for `Competitor`, `ChangeEvent`, `Briefing`, `RevenueContext` live in `frontend/src/types.ts`
- Types must match the shapes in `_docs/plan.md`
EOF
)"

# ---------------------------------------------------------------------------
# 3
create_issue "Build app shell: sidebar, top bar, main area" "$(cat <<'EOF'
## Goal

Every page renders inside a consistent shell with a left sidebar, a top
bar, and a centered main area, matching `_docs/design-system.md`.

## Acceptance criteria

- [ ] Sidebar: 240px, `--surface` bg, items "Competitors" (home) and "Briefing" (latest)
- [ ] Active sidebar item uses `--surface-raised` and a 2px left `--accent` border
- [ ] Top bar: 56px tall, shows page title (H1) and an optional primary action slot
- [ ] Main area: max-width 1100px, centered, 24px padding
- [ ] Shell is keyboard navigable; focus ring visible on sidebar links
- [ ] A layout test asserts sidebar links are present and the title renders

## Out of scope

- Page content (issues #4–#9)
- Mobile layout

## Constraints

- Use React Router (`react-router-dom`) for navigation
- Read `_docs/design-system.md` before writing any CSS
EOF
)"

# ---------------------------------------------------------------------------
# 4
create_issue "Competitors list page with mock data" "$(cat <<'EOF'
## Goal

The home route `/` lists all tracked competitors from `SignalService`,
each row showing name, domain, and last-refreshed time.

## Acceptance criteria

- [ ] Route `/` renders a table of competitors from `SignalService.listCompetitors()`
- [ ] Each row: name, monospace domain, "Last refreshed: <relative time>" or "Never"
- [ ] Rows sorted alphabetically by name
- [ ] Clicking a row navigates to `/competitor/:id`
- [ ] Empty state: "No competitors yet. Add your first competitor." + button to `/add`
- [ ] Loading state: 5 skeleton rows (no spinner)
- [ ] Error state: if the service throws, show "Could not load competitors." + retry button
- [ ] Test covers loading, empty, populated, and error states

## Out of scope

- Search / filter (post-MVP)
- Pagination (post-MVP)

## Constraints

- Use `MockSignalService` through `getSignalService()`
- Follow `_docs/design-system.md` Table and Empty state rules
EOF
)"

# ---------------------------------------------------------------------------
# 5
create_issue "Add competitor form" "$(cat <<'EOF'
## Goal

A user can add a competitor by entering a name, a domain, and optionally
a TrustMRR slug. The form validates input and redirects to the new
competitor's detail page on success.

## Acceptance criteria

- [ ] Route `/add` renders a form with fields: name (required), domain (required), trustmrr_slug (optional)
- [ ] Domain must look like `example.com` or `sub.example.com`; otherwise show inline error
- [ ] Submit button disabled while name or domain is empty, or while submitting
- [ ] On success, navigate to `/competitor/:id` and show a success toast
- [ ] On service error, show an error toast and keep the form values
- [ ] Cancel button returns to `/`
- [ ] Tests cover: happy path, invalid domain, empty required field, submit disabled state

## Out of scope

- Duplicate-domain detection (post-MVP; record as a follow-up issue if needed)
- Editing a competitor (post-MVP)

## Constraints

- No form library; use controlled components
- Follow `_docs/design-system.md` Button and input rules
EOF
)"

# ---------------------------------------------------------------------------
# 6
create_issue "Competitor detail page with tabs" "$(cat <<'EOF'
## Goal

`/competitor/:id` shows a competitor header and three tabs: Changes,
Revenue, Briefing. The page must handle an unknown id gracefully.

## Acceptance criteria

- [ ] Header: name, monospace domain, "Refresh now" primary button, "Delete" danger button
- [ ] Tabs: Changes (default), Revenue, Briefing; active tab has 2px `--accent` underline
- [ ] Unknown id shows a "Competitor not found" empty state with a link to `/`
- [ ] Delete opens a confirmation dialog; on confirm, deletes and navigates to `/`
- [ ] Refresh button calls `refreshCompetitor(id)` and shows a loading state; on error, shows an error toast
- [ ] Tests cover: renders all three tabs, unknown id, delete confirmation, refresh loading state

## Out of scope

- Tab content (issues #7, #9, and revenue context is part of this issue's Revenue tab placeholder only — full revenue is #17 on the backend and will reuse this tab)

## Constraints

- Tabs are in-page state, not separate routes
- Follow `_docs/design-system.md` Badge (severity) and Button rules
EOF
)"

# ---------------------------------------------------------------------------
# 7
create_issue "Change events list with severity badges" "$(cat <<'EOF'
## Goal

The Changes tab lists change events for a competitor, newest first, each
row showing a severity badge, a one-line diff summary, and a timestamp.

## Acceptance criteria

- [ ] Calls `SignalService.listChangeEvents(competitorId)`
- [ ] Rows sorted by `detected_at` descending
- [ ] Each row: severity badge (low/medium/high per design system), diff_summary (single line, truncated with ellipsis), relative timestamp
- [ ] Acknowledged events are visually muted (lower opacity) but still listed
- [ ] Clicking a row expands an inline diff viewer (added/removed lines colored)
- [ ] Empty state: "No changes detected yet. Refresh to check."
- [ ] Loading state: 3 skeleton rows
- [ ] Tests cover: populated, empty, loading, expand/collapse

## Out of scope

- Filtering by severity (post-MVP)
- Full-page diff view (inline only)

## Constraints

- Follow `_docs/design-system.md` Badge, Table, and Diff viewer rules
- Use `MockSignalService`
EOF
)"

# ---------------------------------------------------------------------------
# 8
create_issue "Acknowledge change event action" "$(cat <<'EOF'
## Goal

A user can mark a change event as acknowledged from the Changes tab. The
row becomes visually muted, and the action is persisted through the service.

## Acceptance criteria

- [ ] Each unacknowledged row shows an "Acknowledge" secondary button
- [ ] Clicking it calls `SignalService.acknowledgeChangeEvent(eventId)`
- [ ] On success, the row switches to the acknowledged (muted) style without a full reload
- [ ] On error, show an error toast and leave the row unchanged
- [ ] Acknowledged rows do not show the button
- [ ] Test covers: happy path, error path, button hidden for acknowledged events

## Out of scope

- Bulk acknowledge (post-MVP)

## Constraints

- Use optimistic UI: update the row immediately, revert on error
- Follow `_docs/design-system.md` Button and Toast rules
EOF
)"

# ---------------------------------------------------------------------------
# 9
create_issue "Weekly briefing view" "$(cat <<'EOF'
## Goal

The Briefing tab (and the sidebar's "Briefing" item) shows the latest
weekly briefing: a short summary and a ranked list of top change events.

## Acceptance criteria

- [ ] Sidebar "Briefing" navigates to `/briefing`
- [ ] Page calls `SignalService.getLatestBriefing()`; if none exists, shows an empty state with a "Generate briefing" primary button
- [ ] When a briefing exists: show `week_start`, `summary_text`, and `top_events` as a ranked list with severity badges
- [ ] "Generate briefing" calls `SignalService.generateBriefing()` and replaces the view with the new briefing
- [ ] Loading state: skeleton for summary + 3 event rows
- [ ] Error state: toast + retry button
- [ ] Tests cover: empty, populated, generate, loading, error

## Out of scope

- Historical briefings (post-MVP)

## Constraints

- Follow `_docs/design-system.md` Card, Badge, and Empty state rules
- Briefing `summary_text` is rendered as plain text, not markdown
EOF
)"

# ---------------------------------------------------------------------------
# 10
create_issue "Generate OpenAPI contract from mock service" "$(cat <<'EOF'
## Goal

`openapi.yaml` at the repo root is the single contract between frontend
and backend. It must cover every method in `SignalService`.

## Acceptance criteria

- [ ] `openapi.yaml` is valid OpenAPI 3.1 (validate with `npx @redocly/cli lint openapi.yaml`)
- [ ] Every `SignalService` method maps to an endpoint with method, path, request body, response body, and error responses
- [ ] Schemas defined for Competitor, Snapshot (internal only, may be omitted), ChangeEvent, Briefing, RevenueContext, Error
- [ ] Endpoints that can fail on network have documented 502/504 responses where applicable
- [ ] `openapi.yaml` is committed at the repo root
- [ ] README links to it

## Out of scope

- Auth (single-user MVP)
- Pagination parameters (post-MVP)

## Constraints

- Path names use plural nouns (`/competitors`, `/briefings`)
- All responses are JSON
EOF
)"

# ---------------------------------------------------------------------------
# 11
create_issue "Scaffold FastAPI backend with health endpoint" "$(cat <<'EOF'
## Goal

A `backend/` directory exists with a runnable FastAPI app, Pydantic models
matching `openapi.yaml`, and a `/health` endpoint, so later backend issues
can add routers.

## Acceptance criteria

- [ ] `cd backend && uv sync` installs dependencies
- [ ] `cd backend && uv run uvicorn app.main:app --port 8091` starts the server
- [ ] `GET /health` returns `{"status": "ok"}`
- [ ] `GET /docs` serves the generated OpenAPI UI
- [ ] `cd backend && uv run pytest` passes with at least one test for `/health`
- [ ] Pydantic models exist for Competitor, ChangeEvent, Briefing, RevenueContext, Error
- [ ] `app/main.py` has CORS configured to allow `http://localhost:5173`
- [ ] `pyproject.toml` lists fastapi, uvicorn, pydantic, httpx, pytest, pytest-asyncio

## Out of scope

- Any business endpoint (issues #12–#14)
- Database (issue #16)

## Constraints

- Python 3.12+
- Use `uv` for dependency management
- Follow the module split in `AGENTS.md`: `routers/`, `models.py`, `store/`
EOF
)"

# ---------------------------------------------------------------------------
# 12
create_issue "In-memory store + Competitor CRUD endpoints" "$(cat <<'EOF'
## Goal

The backend supports creating, listing, fetching, and deleting competitors
in an in-memory store, matching `openapi.yaml`.

## Acceptance criteria

- [ ] `POST /competitors` validates and creates a competitor; returns 201 with the created object
- [ ] `POST /competitors` with an invalid domain returns 422 with a body matching the Error schema
- [ ] `GET /competitors` returns all competitors sorted by name
- [ ] `GET /competitors/{id}` returns 404 with the Error schema for unknown ids
- [ ] `DELETE /competitors/{id}` removes the competitor and returns 204; 404 for unknown ids
- [ ] IDs are UUIDs
- [ ] Tests cover: happy path for each, validation error, not-found for GET and DELETE

## Out of scope

- Persistence (issue #16)
- Duplicate-domain detection (post-MVP)

## Constraints

- Store lives in `backend/app/store/competitors.py` and is injectable (so #16 can swap it)
- Use Pydantic models from #11
EOF
)"

# ---------------------------------------------------------------------------
# 13
create_issue "In-memory store + refresh endpoint with mock fetcher" "$(cat <<'EOF'
## Goal

`POST /competitors/{id}/refresh` fetches the competitor's pages through an
injectable fetcher, stores snapshots, detects changes, and creates
ChangeEvents. For this issue the fetcher is mocked.

## Acceptance criteria

- [ ] Refresh calls the fetcher for `pricing`, `changelog`, and `homepage` source types
- [ ] For each page, a Snapshot is stored with `content_hash` (sha256) and `raw_text`
- [ ] If the new hash equals the latest stored hash for that source, no ChangeEvent is created
- [ ] If the hash differs, a ChangeEvent is created with `diff_summary` (unified diff, first 3 hunks max) and a severity
- [ ] Severity heuristic: a changed numeric value → high; a new heading line → medium; otherwise low
- [ ] A fetcher that raises `httpx.TimeoutException` results in a 502 response and no Snapshot
- [ ] `GET /competitors/{id}/changes` returns ChangeEvents newest first
- [ ] `POST /competitors/{id}/changes/{event_id}/acknowledge` marks an event acknowledged
- [ ] Tests cover: first refresh creates snapshots but no events, second identical refresh creates no events, a changed page creates one event with the expected severity, a timeout returns 502, acknowledge happy path and not-found

## Out of scope

- Real HTTP fetching (issue #18)
- Briefing (issue #14)

## Constraints

- Fetcher interface in `backend/app/services/fetcher.py`
- Diff logic in `backend/app/services/diff.py`
- Use `difflib.unified_diff`
- Tests use a fake fetcher from `conftest.py`; no real network
EOF
)"

# ---------------------------------------------------------------------------
# 14
create_issue "In-memory briefing endpoint" "$(cat <<'EOF'
## Goal

`POST /briefings/generate` builds a template-based briefing from the last
7 days of unacknowledged ChangeEvents. `GET /briefings/latest` returns it.

## Acceptance criteria

- [ ] Generate collects unacknowledged events from the last 7 days across all competitors
- [ ] Events sorted by severity (high > medium > low), then `detected_at` desc
- [ ] Briefing `summary_text` is built from a template: "Week of {date}: N changes across M competitors. Top: ..."
- [ ] `top_event_ids` stores up to 10 event IDs in the sorted order
- [ ] `GET /briefings/latest` returns 404 with Error schema when no briefing exists
- [ ] Generating twice in the same week replaces the previous briefing (deterministic)
- [ ] Tests cover: no events → summary says "No changes this week", events → correct ordering and text, latest 404, regenerate replaces

## Out of scope

- LLM summarization (post-MVP)
- Historical briefing list (post-MVP)

## Constraints

- Briefing builder in `backend/app/services/briefing.py`
- Template is a plain Python f-string; no templating library
EOF
)"

# ---------------------------------------------------------------------------
# 15
create_issue "Connect frontend to real backend (HttpSignalService)" "$(cat <<'EOF'
## Goal

The frontend uses `HttpSignalService` against the real FastAPI backend in
development, replacing `MockSignalService` behind the same interface.

## Acceptance criteria

- [ ] `frontend/src/services/HttpSignalService.ts` implements `SignalService` using `fetch`
- [ ] Base URL comes from `import.meta.env.VITE_API_URL`, defaulting to `http://localhost:8091`
- [ ] `getSignalService()` returns `HttpSignalService` when `VITE_USE_MOCK` is unset or false; returns mock when true
- [ ] Every screen still works end-to-end against the real backend
- [ ] A non-2xx response throws an `ApiError` with status and body
- [ ] CORS preflight succeeds from `http://localhost:5173`
- [ ] Tests: `HttpSignalService` unit tests with mocked `fetch` for each method and one error case
- [ ] Manual QA: add competitor → refresh → see change event → generate briefing, against the running backend

## Out of scope

- Auth headers
- Retry logic

## Constraints

- Do not change component code; only the service layer and provider
- If `openapi.yaml` and the backend disagree, fix the backend, then re-check `openapi.yaml`
EOF
)"

# ---------------------------------------------------------------------------
# 16
create_issue "Replace in-memory stores with SQLAlchemy + SQLite" "$(cat <<'EOF'
## Goal

All data is persisted in SQLite via SQLAlchemy, so restarting the backend
preserves competitors, snapshots, change events, and briefings.

## Acceptance criteria

- [ ] `DATABASE_URL` env var controls the connection; default `sqlite:///./signalstack.db`
- [ ] SQLAlchemy models exist for Competitor, Snapshot, ChangeEvent, Briefing, RevenueContext with the fields from `_docs/plan.md`
- [ ] Tables are created on startup if they do not exist (no Alembic needed for MVP)
- [ ] Store modules use the SQLAlchemy session, not Python dicts
- [ ] No raw SQLite-specific SQL anywhere; ORM only
- [ ] Restart test: start server, create data, stop, start, data is still there
- [ ] All existing backend tests still pass against an in-memory SQLite test DB
- [ ] Tests cover: create then read after a new session, cascade delete of snapshots/events when a competitor is deleted, persistence across app restarts (using a temp file DB)

## Out of scope

- Alembic migrations
- Postgres
- Connection pooling tuning

## Constraints

- `backend/app/db.py` owns the engine and session factory
- Tests use `sqlite:///:memory:` via a fixture in `conftest.py`
- No SQLite-specific types (e.g. no JSON1-only features); use `Text` + `json.dumps` if needed
EOF
)"

# ---------------------------------------------------------------------------
# 17
create_issue "Real TrustMRR client with graceful fallback" "$(cat <<'EOF'
## Goal

The Revenue tab shows verified MRR and 30-day growth from TrustMRR when
available, and a neutral fallback when it is not.

## Acceptance criteria

- [ ] `backend/app/services/trustmrr.py` exposes `fetch_revenue(slug) -> RevenueContext | None`
- [ ] Reads `TRUSTMRR_API_KEY` from env; if unset, returns `None` without raising
- [ ] On HTTP 4xx/5xx or timeout, returns `None` and logs a warning
- [ ] `GET /competitors/{id}/revenue` returns 200 with the RevenueContext, or 200 with `null` when unavailable
- [ ] RevenueContext cached in DB with `verified_at`; re-fetch only if older than 24h
- [ ] Frontend Revenue tab shows MRR, 30d growth with a verified badge when present, and "No verified revenue data" otherwise
- [ ] Tests: success (mocked API), missing key, HTTP error, timeout, cache hit within 24h

## Out of scope

- Billing / paying for TrustMRR
- Other revenue sources

## Constraints

- Use `httpx` with a 10s timeout
- Never raise out of `fetch_revenue`; return `None` on any failure
- Do not hardcode the TrustMRR base URL; put it in a constant with an env override
EOF
)"

# ---------------------------------------------------------------------------
# 18
create_issue "Real page fetcher + diff + severity classifier" "$(cat <<'EOF'
## Goal

Refresh uses real HTTP fetching of competitor pages instead of the mock
fetcher. Diffing and severity classification work on real content.

## Acceptance criteria

- [ ] `backend/app/services/fetcher.py` implements `HttpFetcher` using `httpx` with a 10s timeout
- [ ] Fetches `https://{domain}/pricing`, `https://{domain}/changelog`, `https://{domain}`
- [ ] Strips `<script>` and `<style>` content, collapses whitespace, extracts visible text
- [ ] 404 or 4xx on a source is recorded as a skipped source, not a failure of the whole refresh
- [ ] Timeout or connection error on all sources returns 502; on some sources, proceeds with the rest
- [ ] Diff produces a unified diff string truncated to 40 lines
- [ ] Severity classifier: numeric token changed → high; new line starting with a heading-like pattern (ALL CAPS or ending with `:`) → medium; else low
- [ ] Tests use recorded HTML fixtures and a `respx` mock; no live network
- [ ] Manual QA: add a real competitor, refresh twice with a change in between (e.g. edit the fake fixture), see one high-severity event

## Out of scope

- JavaScript-rendered pages (Playwright)
- Robots.txt handling beyond a TODO note
- Rate limiting across competitors (post-MVP)

## Constraints

- Never fetch more than 3 pages per refresh
- Use `respx` for tests, `httpx` for runtime
- Keep `HttpFetcher` behind the same interface as the mock fetcher from #13
EOF
)"

echo "Created 18 MVP issues."