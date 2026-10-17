#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if ! command -v psql >/dev/null 2>&1; then
  sudo DEBIAN_FRONTEND=noninteractive apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
    postgresql postgresql-contrib redis-server python3-venv python3-dev libpq-dev build-essential
fi

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

.venv/bin/pip install --upgrade pip
# backports.asyncio.runner is only for Python <3.11 and is unpinned on 3.12+
grep -v '^backports\.asyncio\.runner==' requirements.txt > /tmp/requirements.cloud.txt
.venv/bin/pip install -r /tmp/requirements.cloud.txt
# Used by rate limiting; not pinned in requirements.txt
.venv/bin/pip install 'redis>=5.0.0'

if [ ! -f .env ]; then
  cat > .env <<'EOF'
DB_URL=postgresql+asyncpg://expense:expense@localhost:5432/expense_tracker
DB_URL_SYNC=postgresql+psycopg://expense:expense@localhost:5432/expense_tracker
JWT_SECRET_KEY=dev-jwt-secret-for-local-development-only
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF
fi
