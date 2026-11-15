from __future__ import annotations
from opentelemetry.metrics import Meter, Observation

_meter = None
_http_requests = _http_duration = None
_competitor_refreshes = _change_events = _briefings_generated = _refresh_failures = None

def set_meter(meter: Meter) -> None:
    global _meter, _http_requests, _http_duration, _competitor_refreshes, _change_events, _briefings_generated, _refresh_failures
    _meter = meter
    _http_requests = meter.create_counter("signalstack_http_requests", description="HTTP requests handled")
    _http_duration = meter.create_histogram("signalstack_http_request_duration_seconds", unit="s", description="HTTP request duration")
    _competitor_refreshes = meter.create_counter("signalstack_competitor_refreshes", description="Competitor refresh attempts")
    _change_events = meter.create_counter("signalstack_change_events", description="Detected competitor changes")
    _briefings_generated = meter.create_counter("signalstack_briefings_generated", description="Generated briefings")
    _refresh_failures = meter.create_counter("signalstack_refresh_failures", description="Failed competitor refreshes")

def record_http_request(method: str, route: str, status: int, duration: float) -> None:
    attrs = {"http_request_method": method, "http_route": route, "http_response_status_code": status}
    if _http_requests is not None: _http_requests.add(1, attrs)
    if _http_duration is not None: _http_duration.record(duration, attrs)

def record_refresh(success: bool, events: int = 0) -> None:
    if _competitor_refreshes is not None: _competitor_refreshes.add(1, {"result": "success" if success else "failure"})
    if not success and _refresh_failures is not None: _refresh_failures.add(1)
    if events and _change_events is not None: _change_events.add(events)

def record_briefing() -> None:
    if _briefings_generated is not None: _briefings_generated.add(1)
