#!/usr/bin/env sh
set -e

alembic upgrade head
python -m app.seed

exec "$@"

