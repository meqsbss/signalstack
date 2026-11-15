from __future__ import annotations

import hmac
import json
import logging
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("signalstack.oncall")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
WEBHOOK_SECRET = os.getenv("ONCALL_WEBHOOK_SECRET", "")

SYSTEM_PROMPT = """You are the SignalStack on-call incident assistant.
Analyze Prometheus/Alertmanager alerts. Return concise JSON with keys:
severity, summary, likely_causes (array), checks (array), safe_actions (array),
escalation (string). Never claim you executed an action. Never recommend deleting
data, disabling security, or making unreviewed production changes. Prefer
read-only diagnostics and rollback only with human approval."""


def analyze_alert(payload: dict) -> dict:
    alerts = payload.get("alerts", [])
    compact = [{
        "name": a.get("labels", {}).get("alertname"),
        "severity": a.get("labels", {}).get("severity"),
        "status": a.get("status"),
        "summary": a.get("annotations", {}).get("summary"),
        "description": a.get("annotations", {}).get("description"),
        "startsAt": a.get("startsAt"),
    } for a in alerts]
    if not OPENAI_API_KEY:
        return {
            "mode": "rules-based-fallback",
            "severity": "human-review-required",
            "summary": "Alert received. AI analysis is not enabled because OPENAI_API_KEY is not configured.",
            "alerts": compact,
            "likely_causes": ["Application error", "Dependency or telemetry service unavailable", "External competitor website timeout"],
            "checks": ["Inspect Grafana dashboard and Prometheus alert expression", "Review API logs in Loki", "Open the relevant trace in Tempo", "Check container health and recent deployment SHA"],
            "safe_actions": ["Restart only an unhealthy stateless container after confirming impact", "Roll back to the last known-good image only with operator approval"],
            "escalation": "Notify the human operator; no automated production changes were made."
        }

    response = httpx.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json={
            "model": OPENAI_MODEL,
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(compact, ensure_ascii=False)},
            ],
        },
        timeout=30.0,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    return {"mode": "openai", **json.loads(content)}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return
        self.send_error(404)

    def do_POST(self):
        if self.path != "/alerts":
            self.send_error(404)
            return
        if WEBHOOK_SECRET:
            supplied = self.headers.get("X-Oncall-Secret", "")
            if not hmac.compare_digest(supplied, WEBHOOK_SECRET):
                self.send_error(401)
                return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            statuses = {a.get("status") for a in payload.get("alerts", [])}
            if statuses == {"resolved"}:
                result = {"mode": "notification", "summary": "Alert resolved.", "alerts": payload.get("alerts", [])}
            else:
                result = analyze_alert(payload)
            logger.info("ON_CALL_RESULT %s", json.dumps(result, ensure_ascii=False))
            body = json.dumps(result, ensure_ascii=False).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except Exception as exc:
            logger.exception("On-call analysis failed")
            body = json.dumps({"error": "analysis_failed", "detail": str(exc)}).encode()
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def log_message(self, fmt, *args):
        logger.info("HTTP %s", fmt % args)


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8099), Handler).serve_forever()
