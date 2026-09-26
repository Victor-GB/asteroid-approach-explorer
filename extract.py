"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""

import csv
import json
from pathlib import Path

from models import CloseApproach, NearEarthObject


def load_neos(neo_csv_path: str | Path) -> list[NearEarthObject]:
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neos: list[NearEarthObject] = []
    with open(neo_csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            neos.append(NearEarthObject(**row))
    return neos


def load_approaches(cad_json_path: str | Path) -> list[CloseApproach]:
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    with open(cad_json_path, newline="", encoding="utf-8") as json_file:
        dataset = json.load(json_file)
    approaches: list[CloseApproach] = []
    fields = dataset["fields"]
    for values in dataset["data"]:
        info = dict(zip(fields, values, strict=True))
        approaches.append(CloseApproach(**info))
    return approaches
