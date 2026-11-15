# SignalStack DevOps

## Environments

The Docker Compose file defines isolated `dev` and `prod` profiles.
Each environment has its own backend/frontend containers and SQLite volume.

Start development:

```bash
docker compose --profile dev up --build -d
```

Open http://localhost:5173. The backend health endpoint is available inside
the Docker network at http://backend-dev:8091/health.

Start production locally:

```bash
docker compose --profile prod up --build -d
```

Open http://localhost:8080. DEV and PROD use separate persistent volumes.

Stop an environment:

```bash
docker compose --profile dev down
docker compose --profile prod down
```

## CI

`.github/workflows/ci.yml` runs backend pytest, frontend Vitest and the
frontend production build. A push to `main` also publishes immutable
commit-SHA images and the moving `dev` tags to GitHub Container Registry.

## Manual promotion

After the DEV image has passed CI, open **Actions → Promote DEV to PROD →
Run workflow**. Enter the commit SHA from the successful CI run. The workflow
retags those exact images as `prod`, without rebuilding them.

Configure the GitHub repository's `production` environment with required
reviewers if an approval gate is desired. The production image tags are
published to GHCR; a production host can pull those tags to deploy them.

## Notes

- Do not commit secrets or production credentials.
- SQLite data is persisted separately in `dev-data` and `prod-data`.
- Observability instrumentation and dashboards are the next implementation
  stage; this commit establishes the environment and delivery foundation.
