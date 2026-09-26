# Extensions and development tooling

This file records the work added to the Udacity *Explore Near-Earth Objects* starter project beyond the required NEO inspection, filtering, querying, and CSV/JSON export behavior. The required application behavior remains available through `main.py`, including its interactive mode.

## Type checking and data contracts

- Added Python type annotations to the NEO models, database, filters, and exporters, and configured mypy to check the five implementation modules.
- Typed filters as callable predicates on `CloseApproach` objects. `limit` uses a generic type parameter so its output retains the input iterator's item type.
- Represented a close approach's NEO as optional until the database links it. Filters and exporters assert that the link exists before using NEO attributes.
- Accepted both string paths and path-like objects in the CSV and JSON writer annotations.

## Local quality checks

- Added Ruff formatting, linting, and import ordering; mypy type checking; pytest with branch coverage; and `pip-audit` for development dependencies.
- Added `scripts/check.sh` to run the complete local quality sequence.
- Added pre-commit hooks for syntax, formatting, linting, whitespace, merge-conflict markers, and accidental private keys. A pre-push hook runs the full quality script.
- Added project configuration and pinned development dependencies, including `.editorconfig`, `.gitattributes`, `.gitignore`, `pyproject.toml`, and `requirements-dev.txt`.

## Repository automation

- Added GitHub Actions quality checks.
- Added Dependabot configuration for dependency updates and a dependency vulnerability audit in the local quality command.

## Verification

On Python 3.12.3, the full quality script passed Ruff, mypy, `pip-audit`, and all 73 supplied tests. Coverage reported 97% across the measured implementation modules. The command-line and interactive inspect and query paths were exercised, and both CSV and JSON exports were checked through the command-line application.

These additions support development and review; they do not add a new user-facing command or change the required export formats. Optional presentation features are outside this submission.
