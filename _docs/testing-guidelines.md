# Testing Guidelines

Every agent that writes or verifies code reads this file first. The goal
is not coverage for its own sake. The goal is: an agent can prove the
acceptance criteria of an issue actually hold.

## Backend (Python / FastAPI)

### Tools
- `pytest` for tests.
- `httpx.AsyncClient` with `ASGITransport` for endpoint tests.
- A separate in-memory SQLite database per test session (`sqlite:///:memory:`)
  via a fixture. Never test against the dev database.
- `respx` (or `monkeypatch` on the httpx client) to mock TrustMRR and
  page fetches. No real network calls in tests.

### Structure