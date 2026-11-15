# SignalStack DevOps, CI/CD and Observability

## Architecture

- **DEV:** Docker Compose profile `dev`, frontend at port 5173, backend on the internal Docker network.
- **PROD:** Docker Compose profile `prod`, frontend at port 8080, backend on the internal Docker network.
- DEV and PROD use separate SQLite volumes (`dev-data` and `prod-data`).
- GitHub Actions runs backend pytest, frontend Vitest and a frontend production build.
- Successful pushes publish immutable commit-SHA images and the moving `dev` tags to GHCR.
- Production promotion re-tags the exact tested SHA as `prod`; it does not rebuild the artifact.

## Run locally

Requirements: Docker Desktop / Docker Engine with the Compose plugin.

```bash
cp .env.example .env
# Edit .env and set a unique GRAFANA_ADMIN_PASSWORD
docker compose --profile dev up --build -d
```

Open:
- SignalStack DEV: http://localhost:5173
- Grafana dashboard: http://localhost:3000 (user: `admin`, password: `.env`)
- Prometheus: http://localhost:9090
- Alertmanager: http://localhost:9093
- Tempo: http://localhost:3200
- Loki API: http://localhost:3100

Run the local PROD profile separately (it has a separate database volume and port):

```bash
docker compose --profile prod up --build -d
```

Open http://localhost:8080.

Stop services:

```bash
docker compose --profile dev down
docker compose --profile prod down
```

Use `docker compose down -v` only if you intentionally want to delete local database and observability data.

## OpenTelemetry

The FastAPI service exports:
- **Traces:** FastAPI request spans and SQLAlchemy database spans to the OTLP Collector.
- **Metrics:** HTTP request count, HTTP request duration, competitor refresh attempts, detected change events, briefing generation and refresh failures.
- **Logs:** Python application logs through the OTLP log pipeline.

The Collector exports metrics for Prometheus, traces to Tempo and logs to Loki. Grafana provisions all three data sources and the SignalStack dashboard automatically.

## Dashboard and alerting

The provisioned dashboard is **SignalStack / Application Observability**. It includes request rate, 5xx rate, competitor refreshes, detected changes, p95 latency, refresh failures and application logs.

Prometheus alert rules:
- `SignalStackHighServerErrorRate`: 5xx responses exceed 5% for 2 minutes.
- `SignalStackRefreshFailures`: more than 2 refresh failures in 10 minutes.
- `SignalStackApiDown`: the telemetry collector is unavailable.

Alertmanager sends firing and resolved alerts to the AI on-call webhook.

## AI on-call responder

The responder receives Alertmanager payloads and records its analysis in the `oncall-agent` container logs. With `OPENAI_API_KEY` configured it uses the OpenAI API to produce likely causes, read-only checks, safe suggested actions and escalation guidance. Without a key it uses a deterministic fallback diagnosis.

The agent is advisory only. It does not restart containers, change infrastructure or perform production remediation automatically. Human approval is required for operational changes.

To enable AI analysis locally, set `OPENAI_API_KEY` in `.env`, then run:

```bash
docker compose up -d --build oncall-agent
docker compose logs -f oncall-agent
```

## CI and DEV images

The workflow is `.github/workflows/ci.yml`. It runs on pushes to `main` and `devops/**`, pull requests to `main`, and manual dispatch. A push triggers image publishing after both test jobs pass.

Images:
- `ghcr.io/meqsbss/signalstack-backend:<commit-sha>`
- `ghcr.io/meqsbss/signalstack-frontend:<commit-sha>`
- `ghcr.io/meqsbss/signalstack-oncall:<commit-sha>`

## Manual DEV to PROD promotion

1. Open **Actions → Promote DEV to PROD → Run workflow**.
2. Enter the full 40-character commit SHA from a successful CI run.
3. The workflow validates the SHA, pulls the already-built images and tags the same images as `prod`.
4. No rebuild happens during promotion.

Configure a GitHub Environment named `production` and add required reviewers if you want a manual approval gate before production promotion.

### Optional remote deployment

The workflow can deploy to a Linux Docker host over SSH when these repository settings exist:

**Actions → Variables**
- `DEPLOY_HOST`: server hostname or IP
- `DEPLOY_USER`: SSH user

**Actions → Secrets**
- `DEPLOY_SSH_KEY`: private key for that user
- `GRAFANA_ADMIN_PASSWORD`: strong Grafana password
- `OPENAI_API_KEY`: optional, for AI-generated incident analysis
- `ONCALL_WEBHOOK_SECRET`: optional shared webhook secret

The server must have Docker Engine and the Compose plugin installed, SSH access enabled, and outbound access to GHCR. The workflow copies `compose.prod.yml` and the `observability/` configuration, writes a server-side `.env`, logs in to GHCR and starts the production stack.

The remote application is exposed on port 8080 and Grafana on port 3000. Put a TLS reverse proxy and firewall in front of these services before exposing them to the public internet.

## Safety

- Never commit `.env`, API keys, SSH keys or production credentials.
- DEV and PROD data volumes are separate.
- Promotion uses the same immutable commit-SHA images that passed CI.
- The on-call agent provides recommendations only; it does not autonomously modify production.
