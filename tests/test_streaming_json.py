"""Check streaming JSON export behaviour."""

import json
from pathlib import Path

from write import write_to_json


def test_empty_stream_writes_empty_array(tmp_path: Path) -> None:
    """Write an empty result stream as a valid JSON array."""
    output = tmp_path / "empty.json"

    write_to_json(iter(()), output)

    with output.open(encoding="utf-8") as json_file:
        assert json.load(json_file) == []
