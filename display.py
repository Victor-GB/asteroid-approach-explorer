"""Display close approaches in terminal tables."""

from collections.abc import Iterable
from math import isnan

from rich.console import Console
from rich.table import Table

from models import CloseApproach

CLOSE_APPROACH_HEADERS = (
    "Designation",
    "Name",
    "Approach time (UTC)",
    "Distance (au)",
    "Velocity (km/s)",
    "Diameter (km)",
    "Potentially hazardous",
)


def display_approaches(results: Iterable[CloseApproach]) -> None:
    """Display the supplied close approaches in a table.

    :param results: Close approaches already limited by the caller.
    """
    table = Table(title="Close approaches")
    for head in CLOSE_APPROACH_HEADERS:
        table.add_column(head)

    for approach in results:
        neo = approach.neo
        assert neo is not None, "CloseApproach object has no linked NEO."
        dist = f"{approach.distance:.6f}"
        speed = f"{approach.velocity:.2f}"
        hazard = "Yes" if neo.hazardous else "No"
        diameter = "Unknown" if isnan(neo.diameter) else f"{neo.diameter:.3f}"
        table.add_row(
            neo.designation,
            neo.name or "Unnamed",
            approach.time_str,
            dist,
            speed,
            diameter,
            hazard,
        )
    Console().print(table)
