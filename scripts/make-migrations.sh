#!/bin/sh -e

exec alembic -c /src/alembic.ini revision --autogenerate
