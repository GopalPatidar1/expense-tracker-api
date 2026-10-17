#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

ROOT="$(pwd)"
VENV="${ROOT}/.venv"

start_postgres() {
  if ! sudo service postgresql status >/dev/null 2>&1; then
    sudo service postgresql start
  else
    sudo service postgresql start || true
  fi
  for _ in $(seq 1 30); do
    if sudo -u postgres pg_isready -q 2>/dev/null; then
      return 0
    fi
    sleep 1
  done
  echo "PostgreSQL did not become ready in time" >&2
  return 1
}

ensure_db_role() {
  sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='expense'" | grep -q 1 \
    || sudo -u postgres psql -c "CREATE USER expense WITH PASSWORD 'expense';"
  sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='expense_tracker'" | grep -q 1 \
    || sudo -u postgres psql -c "CREATE DATABASE expense_tracker OWNER expense;"
  sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE expense_tracker TO expense;" >/dev/null
}

start_redis() {
  if redis-cli ping >/dev/null 2>&1; then
    return 0
  fi
  sudo service redis-server start || true
  for _ in $(seq 1 30); do
    if redis-cli ping >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
  done
  echo "Redis did not become ready in time" >&2
  return 1
}

start_postgres
ensure_db_role
start_redis

"${VENV}/bin/alembic" upgrade head

if ! curl -sf http://127.0.0.1:8000/health >/dev/null 2>&1; then
  exec "${VENV}/bin/uvicorn" app.main:app --host 0.0.0.0 --port 8000
fi
