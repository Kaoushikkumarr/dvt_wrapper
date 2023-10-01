#!/usr/bin/env bash
set -euo pipefail

ddtrace-run \
  gunicorn \
  "${PROJECT_ROOT_IMPORT_NAME}.app:create_app()" \
  -b ":${GUNICORN_PORT}" \
  -w "${GUNICORN_WORKERS}" \
  -k "${GUNICORN_WORKER_CLASS}" \
  --log-level="${GUNICORN_LOG_LEVEL}" \
  --logger-class="${GUNICORN_LOGGER_CLASS}" \
  --worker-connections="${GUNICORN_WORKER_CONNECTIONS}" \
  --max-requests="${GUNICORN_MAX_REQUESTS}" \
  --max-requests-jitter="${GUNICORN_MAX_REQUESTS_JITTER}"
