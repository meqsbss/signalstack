# Brainstorm — How SignalStack was scoped

This is the raw thinking that led to `plan.md`. It is kept in the repo so
future contributors (human or agent) can see why decisions were made.

## Starting point

The brief was: "Pick a project idea, different from Part I, and come up
with a non-trivial app. No habit tracker, no to-do list. An idea you'd be
proud to show off."

I looked at TrustMRR (trustmrr.com) for inspiration about what indie
founders actually pay for. The leaderboard showed SaaS tools that help
people find prospects, validate data, schedule content, and attribute ad
spend. The common thread: **founders pay for signal, not storage.**

I ruled out:

- Another CRM (crowded, boring).
- A URL shortener (trivial).
- An AI chatbot wrapper (no substance).
- A dashboard that only reads static data (no pipeline).

## The idea

Competitive intelligence for indie SaaS founders. The pitch:

> Know what your competitors shipped, priced, and how fast they're growing
> — without manually checking ten tabs every week.

Why this is non-trivial:

- It has an **ingestion pipeline**: fetch pages, hash content, diff
  snapshots.
- It does **entity resolution**: match a competitor domain to a TrustMRR
  startup.
- It does **prioritization**: classify severity, rank events, build a
  briefing.
- It has **graceful degradation**: TrustMRR may be down; the app must
  still work.

## Questions I asked myself (one at a time)

**Q: Who is the user?**
A: A solo indie founder or a two-person team. They track 3–10 competitors.
They do a 10-minute review on Monday morning.

**Q: What does "competitor change" mean?**
A: A change in the visible text of a pricing page, changelog, or homepage.
Not pixel diffs. Not JS-rendered content (out of scope for MVP — we fetch
static HTML).

**Q: How is severity decided?**
A: Heuristics, not AI, for the MVP:
- Price number changed → high.
- A new section heading appeared → medium.
- Only copy/wording changed → low.
This keeps the MVP deterministic and testable. LLM summarization is
post-MVP.

**Q: Do we need auth?**
A: No. Single-user local app. Auth is post-MVP.

**Q: Where does revenue data come from?**
A: TrustMRR. The user optionally provides a slug. If the API is
unavailable or the slug is missing, the revenue tab shows a neutral
fallback. Revenue is context, not the core feature — the core feature is
change detection.

**Q: How often do we refresh?**
A: In the MVP, only on demand (a "Refresh now" button). Scheduled
scraping is post-MVP because it needs a job runner and raises
operational questions (rate limits, robots.txt) that are out of scope
for a first version.

**Q: Frontend-first or backend-first?**
A: Frontend-first, following the AI Shipping blog approach. Build the
dashboard against a `MockSignalService`, then freeze the contract in
`openapi.yaml`, then build the backend in-memory, then add SQLite.

**Q: How do we keep quality high with an AI agent?**
A: Adopt the PM → Engineer → QA loop from the AI-Native Development
article. GitHub Issues are the backlog. Every issue is groomed before
implementation and verified by QA before it is closed.

## Tech stack decision

| Layer | Choice | Why |
|-------|--------|-----|
| Frontend | React + TypeScript + Vite | Fast, well-known to coding agents, easy mock service layer |
| Backend | FastAPI (Python) | Typed, fast to build, generates OpenAPI automatically |
| ORM | SQLAlchemy | DB-agnostic; SQLite now, Postgres later without rewrites |
| DB | SQLite | Zero-config local persistence for MVP |
| Fetching | httpx | Simple, async-capable, timeouts easy |
| Diffing | Python `difflib` | Stdlib, no dependency |
| Design | Claude Design output, recorded in `design-system.md` | Non-generic design tokens the agent can follow |

## What I deliberately left out of MVP

- Cron / scheduled refresh
- LLM summarization
- Reddit / HN sentiment
- Notifications
- Auth
- Postgres / Docker
- CI/CD

Each of these is filed mentally as post-MVP and will become a
`post-mvp` labeled issue in the backlog.

## Definition of "done" for the whole project

- All `mvp` issues closed after QA PASS.
- All `user-test-bug` issues closed after QA PASS.
- App runs locally: `make run-backend` + `make run-frontend`.
- Data survives a backend restart.
- TrustMRR fallback verified by unsetting the API key.