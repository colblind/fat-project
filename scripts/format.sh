#!/bin/sh -e
set -x

ruff --fix src
ruff format src