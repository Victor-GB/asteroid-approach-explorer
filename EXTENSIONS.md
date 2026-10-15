# Implementation and portfolio enhancements

## My contribution

I implemented the core application tasks: NEO models, CSV/JSON extraction, database construction and linking, object lookups, close-approach queries, concrete filters, result limiting and CSV/JSON exports.

Udacity supplied the project scaffold, command-line and interactive framework, base filter scaffold, helper utilities, datasets and regression tests. The original project brief is preserved in [UDACITY_PROJECT.md](UDACITY_PROJECT.md).

I then extended the application and development workflow as described below.

## Rich terminal output

- Added a separate seven-column renderer with units and readable unknown values.
- Made Rich tables the default when the optional dependency is installed, retaining plain-text output otherwise.
- Applied result limits before rendering and kept exports independent of presentation.
- Added three focused display tests.

## CLI validation and error handling

- Added converters for finite, non-negative physical bounds and non-negative integer limits.
- Preserved zero as the unlimited-results setting.
- Rejected reversed date, distance, velocity and diameter ranges while allowing equal or omitted bounds.
- Kept range rejection at the CLI boundary, preserving the supplied query API behaviour.
- Added useful errors for unreadable files, malformed input, unsupported export extensions and failed writes.
- Kept the interactive shell available after invalid commands.

## Forgiving object lookups

Name and designation matching ignores case and surrounding whitespace. Normalised dictionary keys support these lookups while preserving the original model values for display and export.

Two focused tests check matching and preservation of the original values.

## Streaming JSON export

JSON export writes each entry incrementally instead of collecting the entire export in another list. The existing JSON array, nested NEO objects and `NaN` convention for unknown diameters are preserved.

The database remains in memory; the improvement concerns the additional memory needed during export. A focused test covers an empty result stream, alongside the supplied export compatibility tests.

## Type checking and data contracts

- Added annotations across the application and tests.
- Configured project-wide mypy checks, retaining the explicit exception for the supplied helper module.
- Expressed filters as callable predicates and made result limiting generic over iterable element types.
- Represented unlinked NEO relationships as optional.
- Corrected `limit()` annotations to reflect its existing support for both iterables and iterators.
- Added typed test fixtures and preserved the supplied regression assertions.
- Reworked the export-test buffer helper using a scoped mock while retaining its in-memory testing approach.

## Quality checks and automation

- Configured Ruff formatting, lint and import-order checks.
- Added pytest branch-coverage reporting and dependency auditing for development and Rich requirements.
- Created `scripts/check.sh` as the shared local and CI quality command.
- Added commit checks and a full-quality pre-push hook.
- Expanded GitHub Actions from baseline-only testing to the complete quality sequence.
- Added portable Bash development shortcuts with recorded logs.
- Pinned development and presentation dependencies.

The supplied helper and original regression-test files retain their documented Ruff exclusions.

## Repository security

- Configured weekly Dependabot version updates for Python packages and GitHub Actions.
- Enabled Dependabot vulnerability alerts and security-update PRs.
- Enabled GitHub-managed CodeQL default setup for Python and GitHub Actions.
- Enabled secret scanning and push protection.
- Included dependency vulnerability auditing in local and CI checks, and private-key detection in commit hooks.

Dependency-update PRs are reviewed and checked before merging. These repository settings complement the controls stored in Git.

## Verification evidence

The latest recorded full local suite passed **102 tests**, with **87% configured core coverage**. Coverage measures the database, extraction, filters, models and export modules.

Project-wide mypy passed across **20 source files**. GitHub quality checks passed for the enhancement PRs and the subsequent mypy and Ruff updates. The initial CodeQL setup and analysis also completed successfully.

Manual checks exercised direct and interactive commands, invalid values and ranges, malformed input, export failures, valid queries and forgiving lookups.
