#!/usr/bin/env bash

export PY_PROJECT_ROOT="$(realpath -- "$(dirname -- "${BASH_SOURCE[0]}")/..")"

frma() (
    cd "$PY_PROJECT_ROOT" || return
    local project_python="$PY_PROJECT_ROOT/.venv/bin/python"

    "$project_python" -m ruff check --fix --exit-zero . || return
    "$project_python" -m ruff format . || return
    "$project_python" -m ruff check .
)

frmpya() (
    frma || return
    cd "$PY_PROJECT_ROOT" || return
    "$PY_PROJECT_ROOT/.venv/bin/python" -m mypy .
)

_latest_python_file() {
    find "$PWD" -maxdepth 1 -type f -name '*.py' -printf '%T@ %p\n' |
        sort -nr |
        sed -n '1s/^[^ ]* //p'
}

frmal() (
    set -o pipefail
    mkdir -p "$PY_PROJECT_ROOT/tmp" || return
    frma 2>&1 | tee "$PY_PROJECT_ROOT/tmp/frma.log"
)

frmpyal() (
    set -o pipefail
    mkdir -p "$PY_PROJECT_ROOT/tmp" || return
    frmpya 2>&1 | tee "$PY_PROJECT_ROOT/tmp/frmpya.log"
)

frm() (
    local target
    target="${1:-$(_latest_python_file)}"

    if [[ -z "$target" ]]; then
        printf 'No Python files in the current directory.\n'
        return 1
    fi

    local display_path="${target#"$PY_PROJECT_ROOT"/}"
    printf 'Selected: %s/%s\n' "${PY_PROJECT_ROOT##*/}" "$display_path"
    cd "$PY_PROJECT_ROOT" || return
    local project_python="$PY_PROJECT_ROOT/.venv/bin/python"

    "$project_python" -m ruff check --fix --exit-zero "$target" || return
    "$project_python" -m ruff format "$target" || return
    "$project_python" -m ruff check "$target"
)

frmpy() (
    local target
    target=$(_latest_python_file)

    frm "$target" || return
    cd "$PY_PROJECT_ROOT" || return
    "$PY_PROJECT_ROOT/.venv/bin/python" -m mypy "$target"
)


pt() (
    local target
    target=$(_latest_python_file)

    if [[ -z "$target" ]]; then
        printf 'No Python files in the current directory.\n'
        return 1
    fi

    local display_path="${target#"$PY_PROJECT_ROOT"/}"
    printf 'Selected: %s/%s\n' "${PY_PROJECT_ROOT##*/}" "$display_path"
    cd "$PY_PROJECT_ROOT" || return
    "$PY_PROJECT_ROOT/.venv/bin/python" -m pytest -q "$target"
)

pta() (
    cd "$PY_PROJECT_ROOT" || return
    "$PY_PROJECT_ROOT/.venv/bin/python" -m pytest -q
)

ptl() (
    set -o pipefail
    mkdir -p "$PY_PROJECT_ROOT/tmp" || return
    pt 2>&1 | tee "$PY_PROJECT_ROOT/tmp/pytest-latest.log"
)

ptal() (
    set -o pipefail
    mkdir -p "$PY_PROJECT_ROOT/tmp" || return
    pta 2>&1 | tee "$PY_PROJECT_ROOT/tmp/pytest-all.log"
)

cdt() {
    cd "$PY_PROJECT_ROOT/tests"
}

cdr() {
    cd "$PY_PROJECT_ROOT"
}

cds() {
    cd "$PY_PROJECT_ROOT"
}
o() {
    code -r "$@"
}

al() {
    cat <<'HELP'
frm     Fix and format the newest Python file in the current directory.
frmpy   Same as frm, then run mypy on that file.
frma    Fix and format Python files recursively under PY_PROJECT_ROOT.
frmal   Same as frma, saving output to tmp/frma.log.
frmpya  Same as frma, then run mypy across the project.
frmpyal Same as frmpya, saving output to tmp/frmpya.log.
pt      Run pytest on the newest Python file in the current directory.
pta     Run the complete project test suite.
ptl     Same as pt, saving output to tmp/pytest-latest.log.
ptal    Same as pta, saving output to tmp/pytest-all.log.
cdt     Change to the project's tests directory.
cdr     Change to the project root directory.
cds     Change to the project's root directory.
o       Open files in the current VS Code window: o filename
al      Show this shortcut reference.
HELP
}
