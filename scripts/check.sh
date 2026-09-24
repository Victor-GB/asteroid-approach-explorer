#!/usr/bin/env bash

set -euo pipefail

printf '\n==> Ruff formatting\n'
ruff format --check .

printf '\n==> Ruff linting\n'
ruff check .

printf '\n==> Mypy type checking\n'
mypy

printf '\n==> Dependency vulnerability audit\n'
python -m pip_audit --strict -r requirements-dev.txt

printf '\n==> Pytest and coverage\n'
pytest -q --tb=short
