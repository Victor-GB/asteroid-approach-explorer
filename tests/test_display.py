"""Test Rich terminal presentation."""

from pytest import CaptureFixture, MonkeyPatch

from display import display_approaches
from models import CloseApproach, NearEarthObject


def test_display_missing_values(capsys: CaptureFixture[str]) -> None:
    """Verify readable labels for missing names and diameters."""
    neo = NearEarthObject(pdes="TEST-1", name="", diameter="", pha="N")
    approach = CloseApproach(
        des="TEST-1",
        cd="2020-Jan-01 00:00",
        dist="0.1",
        v_rel="5",
    )
    approach.neo = neo
    display_approaches([approach])
    output = capsys.readouterr().out

    assert "TEST-1" in output
    assert "Unnamed" in output
    assert "Unknown" in output
    assert "nan" not in output.lower()


def test_display_known_values(capsys: CaptureFixture[str]) -> None:
    """Verify names, hazardous status and rounded measurements."""
    neo = NearEarthObject(pdes="TEST-2", name="Example", diameter="1.23456", pha="Y")
    approach = CloseApproach(
        des="TEST-2",
        cd="2020-Jan-01 00:00",
        dist="0.123456789",
        v_rel="12.346",
    )
    approach.neo = neo
    display_approaches([approach])
    output = capsys.readouterr().out

    assert "TEST-2" in output
    assert "Example" in output
    assert "Yes" in output
    assert "1.235" in output
    assert "0.123457" in output
    assert "12.35" in output


def test_display_empty_results(
    capsys: CaptureFixture[str], monkeypatch: MonkeyPatch
) -> None:
    """Verify empty results display table headings without errors."""
    monkeypatch.setenv("COLUMNS", "160")
    display_approaches([])
    captured = capsys.readouterr()

    assert "Close approaches" in captured.out
    assert "Designation" in captured.out
    assert captured.err == ""
