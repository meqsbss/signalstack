from __future__ import annotations

import logging
import os
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

from app.db import engine, init_db
from app.observability import record_http_request, set_meter
from app.routers import briefings, changes, competitors
from app.services.fetcher import HttpFetcher

resource = Resource.create({
    "service.name": os.getenv("OTEL_SERVICE_NAME", "signalstack-api"),
    "service.version": "0.1.0",
    "deployment.environment": os.getenv("APP_ENV", "development"),
})
endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317")
headers = os.getenv("OTEL_EXPORTER_OTLP_HEADERS")

tracer_provider = TracerProvider(resource=resource)
tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, headers=headers)))
trace.set_tracer_provider(tracer_provider)

metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint=endpoint, headers=headers),
    export_interval_millis=15000,
)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)
set_meter(metrics.get_meter("signalstack.api", "0.1.0"))

logger_provider = LoggerProvider(resource=resource)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter(endpoint=endpoint, headers=headers)))
logging.getLogger().addHandler(LoggingHandler(level=logging.INFO, logger_provider=logger_provider))
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logging.getLogger().setLevel(os.getenv("LOG_LEVEL", "INFO"))

app = FastAPI(title="SignalStack API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:8080").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.fetcher = HttpFetcher()
app.include_router(competitors.router)
app.include_router(changes.router)
app.include_router(changes.events_router)
app.include_router(briefings.router)


@app.on_event("startup")
async def on_startup() -> None:
    init_db()
    SQLAlchemyInstrumentor().instrument(engine=engine)


FastAPIInstrumentor.instrument_app(app)


@app.middleware("http")
async def collect_http_metrics(request: Request, call_next):
    started = time.perf_counter()
    status = 500
    try:
        response = await call_next(request)
        status = response.status_code
        return response
    finally:
        route = request.scope.get("route")
        route_name = getattr(route, "path", "unmatched")
        record_http_request(request.method, route_name, status, time.perf_counter() - started)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
async def ready() -> dict[str, str]:
    return {"status": "ready"}
