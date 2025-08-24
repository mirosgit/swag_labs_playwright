#!/usr/bin/env bash
set -euo pipefail

mkdir -p /app/allure-results /app/traces

SUITE="${TEST_SUITE:-all}"
ARGS="${PYTEST_ARGS:-}"

echo "[ENTRYPOINT] TEST_SUITE=${SUITE} ; PYTEST_ARGS=${ARGS:-<none>} ; HEADLESS=${HEADLESS:-<not set>}"

case "${SUITE}" in
  smoke)
    exec pytest -q -m smoke ${ARGS}
    ;;
  regression)
    exec pytest -q -m regression ${ARGS}
    ;;
  all|*)
    exec pytest -q ${ARGS}
    ;;
esac
