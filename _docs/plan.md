# SignalStack — Product Specification

## Problem

Indie SaaS founders need to know what their competitors are doing: pricing
changes, new features, changelog updates, and whether the competitor is
actually growing (verified revenue, not vanity metrics). Today this
requires manually checking competitor pages, Reddit, and TrustMRR. It is
tedious and easy to miss.

## Solution

SignalStack is a single-user local dashboard that:

1. Tracks a list of competitors (domain + optional TrustMRR slug).
2. Captures snapshots of public competitor pages (pricing, changelog,
   homepage).
3. Detects meaningful changes between snapshots and classifies severity.
4. Enriches each competitor with verified revenue context from TrustMRR.
5. Produces a weekly briefing listing the top changes to review.

## Personas

**Indie founder (primary user).** Solo developer or small team. Wants a
10-minute weekly review of what competitors shipped and whether it
threatens them. Not a data analyst. Values signal over noise.

## Core entities

| Entity | Key fields |
|--------|-----------|
| Competitor | id, name, domain, trustmrr_slug (nullable), created_at |
| Snapshot | id, competitor_id, source_type, content_hash, raw_text, fetched_at |
| ChangeEvent | id, competitor_id, snapshot_id, diff_summary, severity, detected_at, acknowledged |
| Briefing | id, week_start, summary_text, top_event_ids, created_at |
| RevenueContext | id, competitor_id, mrr, growth_30d, verified_at, source |

`source_type` ∈ {pricing, changelog, homepage}
`severity` ∈ {low, medium, high}

## User flows

### Flow 1 — Add a competitor
1. User clicks "Add competitor".
2. Enters name, domain, optional TrustMRR slug.
3. System validates the domain format and saves the competitor.
4. Competitor appears in the list with status "Never refreshed".

### Flow 2 — Refresh a competitor
1. User opens a competitor detail page.
2. Clicks "Refresh now".
3. System fetches pricing/changelog/homepage pages.
4. For each page, computes content hash.
5. If hash differs from the latest snapshot, creates a new Snapshot and
   a ChangeEvent with a text diff summary and a severity.
6. UI shows the new events.

### Flow 3 — Review change events
1. User opens the competitor detail page → Changes tab.
2. Sees a list of change events, newest first, with severity badges.
3. Can click an event to see the full diff.
4. Can mark an event as acknowledged (reduces noise on the dashboard).

### Flow 4 — View revenue context
1. On the competitor detail page → Revenue tab.
2. If a TrustMRR slug is set and the API returns data, show MRR and 30d
   growth with a "verified via TrustMRR" badge.
3. If no slug or API fails, show a neutral "No verified revenue data"
   state. Never block the rest of the page.

### Flow 5 — Generate weekly briefing
1. User clicks "Generate briefing".
2. System collects all unacknowledged change events from the last 7 days.
3. Sorts by severity (high first), then by detected_at (newest first).
4. Builds a template-based summary: one line per top event.
5. Saves a Briefing and shows it.

## MVP scope (in)

- Competitor CRUD (create, list, view, delete)
- Manual "Refresh now" per competitor (real HTTP fetch)
- Snapshot + content-hash diff detection
- ChangeEvent creation with heuristic severity
- Change event list and detail
- Acknowledge event action
- Revenue context from TrustMRR (with graceful fallback)
- Weekly briefing generation (template-based)
- SQLite persistence via SQLAlchemy
- Single-user local app (no auth)

## Out of scope (post-MVP)

- Automated scheduled scraping (cron / APScheduler)
- LLM-powered change summarization
- Reddit / Hacker News sentiment ingestion
- Email or Slack notifications
- Multi-user auth
- Postgres / Docker Compose deployment
- CI/CD pipeline

## Non-functional requirements

- All backend data access through SQLAlchemy ORM. No raw SQLite SQL.
- `DATABASE_URL` env var controls the DB connection.
- `TRUSTMRR_API_KEY` env var (optional). If unset, revenue tab shows
  the fallback state.
- Every backend endpoint appears in `openapi.yaml`.
- Frontend talks to the backend only through `services/SignalService.ts`.
- Fetch timeouts: 10 seconds per page. On timeout, record the failure,
  do not create a Snapshot.

## Success criteria (for MVP)

- A user can add 3 competitors, refresh them, see detected changes with
  severity, view revenue context, and generate a briefing.
- Stopping and restarting the backend preserves all data.
- If TrustMRR is unreachable, the app still works and shows a fallback.

## Status

**MVP completed.** All 18 `mvp` issues closed after QA PASS. One
`user-test-bug` issue (#19) found during manual testing, fixed, and closed.
17 backend tests and 18 frontend tests pass. `openapi.yaml` generated.