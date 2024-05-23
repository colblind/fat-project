#!/usr/bin/env bash

set -e

DEFAULT_MODULE_NAME=config.app.instance

MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-get_app_instance}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
LOG_LEVEL=${LOG_LEVEL:-info}
LOG_CONFIG=${LOG_CONFIG:-/src/logging.ini}

# Make migrations
sh ./scripts/make-migrations.sh

# Run migrations
sh ./scripts/run-migrations.sh

# Start Uvicorn with live reload
exec uvicorn --reload --proxy-headers --host $HOST --port $PORT --log-config $LOG_CONFIG --factory "$APP_MODULE"