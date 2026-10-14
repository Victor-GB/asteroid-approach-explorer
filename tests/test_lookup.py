"""Check forgiving NEO lookups."""

from database import NEODatabase
from models import NearEarthObject


def test_name_lookup_ignores_case_and_spaces() -> None:
    """Find an NEO while preserving its original name."""
    neo = NearEarthObject(pdes="1P", name="Halley", pha="N")
    database = NEODatabase([neo], [])

    assert database.get_neo_by_name("  hAlLeY  ") is neo
    assert neo.name == "Halley"


def test_designation_lookup_ignores_case_and_spaces() -> None:
    """Find an NEO while preserving its original designation."""
    neo = NearEarthObject(pdes="1P", name="Halley", pha="N")
    database = NEODatabase([neo], [])

    assert database.get_neo_by_designation("  1p  ") is neo
    assert neo.designation == "1P"
