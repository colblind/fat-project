#!/bin/sh -e

exec alembic -c /src/alembic.ini upgrade head
