"""Check CLI query validation."""

import argparse
from datetime import date
from pathlib import Path

import pytest

from main import make_parser, non_negative_float, non_negative_int, validate_query_args


def test_physical_bound_accepts_zero() -> None:
    """Accept zero as a physical bound."""
    assert non_negative_float("0") == 0.0


def test_physical_bound_accepts_positive_value() -> None:
    """Accept a positive physical bound."""
    assert non_negative_float("2.5") == 2.5


def test_physical_bound_rejects_negative_value() -> None:
    """Reject a negative physical bound."""
    with pytest.raises(argparse.ArgumentTypeError):
        non_negative_float("-1")


def test_physical_bound_rejects_nan() -> None:
    """Reject NaN as a physical bound."""
    with pytest.raises(argparse.ArgumentTypeError):
        non_negative_float("nan")


def test_physical_bound_rejects_infinity() -> None:
    """Reject infinity as a physical bound."""
    with pytest.raises(argparse.ArgumentTypeError):
        non_negative_float("inf")


def test_physical_bound_rejects_non_numeric_text() -> None:
    """Reject non-numeric text as a physical bound."""
    with pytest.raises(argparse.ArgumentTypeError):
        non_negative_float("invalid")


def test_limit_accepts_zero() -> None:
    """Accept zero as a result limit."""
    assert non_negative_int("0") == 0


def test_limit_accepts_positive_integer() -> None:
    """Accept a positive integer as a result limit."""
    assert non_negative_int("3") == 3


def test_limit_rejects_negative_integer() -> None:
    """Reject a negative result limit."""
    with pytest.raises(argparse.ArgumentTypeError):
        non_negative_int("-1")


def test_limit_rejects_fractional_value() -> None:
    """Reject a fractional result limit."""
    with pytest.raises(argparse.ArgumentTypeError):
        non_negative_int("1.5")


def test_limit_rejects_non_numeric_text() -> None:
    """Reject non-numeric text as a result limit."""
    with pytest.raises(argparse.ArgumentTypeError):
        non_negative_int("invalid")


def test_query_accepts_omitted_bounds() -> None:
    """Accept a query with no bounds supplied."""
    _, _, query_parser = make_parser()
    args = query_parser.parse_args([])

    validate_query_args(args)


def test_query_accepts_equal_distance_bounds() -> None:
    """Accept equal distance bounds."""
    _, _, query_parser = make_parser()
    args = query_parser.parse_args([])
    args.distance_min = 0.1
    args.distance_max = 0.1

    validate_query_args(args)


def test_query_rejects_reversed_distance_bounds() -> None:
    """Reject a minimum distance greater than the maximum."""
    _, _, query_parser = make_parser()
    args = query_parser.parse_args([])
    args.distance_min = 0.2
    args.distance_max = 0.1

    with pytest.raises(ValueError, match="--min-distance"):
        validate_query_args(args)


def test_query_accepts_equal_velocity_bounds() -> None:
    """Accept equal velocity bounds."""
    _, _, query_parser = make_parser()
    args = query_parser.parse_args([])
    args.velocity_min = 1
    args.velocity_max = 1

    validate_query_args(args)


def test_query_rejects_reversed_velocity_bounds() -> None:
    """Reject a minimum velocity greater than the maximum."""
    _, _, query_parser = make_parser()
    args = query_parser.parse_args([])
    args.velocity_min = 2
    args.velocity_max = 1

    with pytest.raises(ValueError, match="--min-velocity"):
        validate_query_args(args)


def test_query_accepts_equal_diameter_bounds() -> None:
    """Accept equal diameter bounds."""
    _, _, query_parser = make_parser()
    args = query_parser.parse_args([])
    args.diameter_min = 1
    args.diameter_max = 1

    validate_query_args(args)


def test_query_rejects_reversed_diameter_bounds() -> None:
    """Reject a minimum diameter greater than the maximum."""
    _, _, query_parser = make_parser()
    args = query_parser.parse_args([])
    args.diameter_min = 2
    args.diameter_max = 1

    with pytest.raises(ValueError, match="--min-diameter"):
        validate_query_args(args)


def test_query_accepts_equal_date_bounds() -> None:
    """Accepts equal date bounds."""
    _, _, query_parser = make_parser()
    args = query_parser.parse_args([])
    args.start_date = date(2020, 1, 1)
    args.end_date = date(2020, 1, 1)
    validate_query_args(args)


def test_query_rejects_reversed_date_bounds() -> None:
    """Reject a start date greater than end date."""
    _, _, query_parser = make_parser()
    args = query_parser.parse_args([])
    args.start_date = date(2020, 1, 2)
    args.end_date = date(2020, 1, 1)
    with pytest.raises(ValueError, match="--start-date"):
        validate_query_args(args)


def test_query_accepts_csv_export_extension() -> None:
    """Accept a CSV output filename."""
    _, _, query_parser = make_parser()
    args = query_parser.parse_args([])
    args.outfile = Path("results.csv")

    validate_query_args(args)


def test_query_accepts_json_export_extension() -> None:
    """Accept a json output filename."""
    _, _, query_parser = make_parser()
    args = query_parser.parse_args([])
    args.outfile = Path("results.json")

    validate_query_args(args)


def test_query_rejects_txt_export_extension() -> None:
    """Reject an unsupported TXT output filename."""
    _, _, query_parser = make_parser()
    args = query_parser.parse_args([])
    args.outfile = Path("results.txt")

    with pytest.raises(ValueError, match="--outfile"):
        validate_query_args(args)
