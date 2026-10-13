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
    try:
        with open(neo_csv_path, newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file, strict=True)

            fieldnames = reader.fieldnames
            if (
                fieldnames is None
                or "pdes" not in fieldnames
                or "pha" not in fieldnames
            ):
                raise ValueError(
                    f"NEO CSV '{neo_csv_path}' must include 'pdes' and 'pha' columns."
                )
            for row in reader:
                if None in row or None in row.values():
                    raise ValueError(
                        f"NEO CSV '{neo_csv_path}' has a row that does not match its header."
                    )

                neos.append(NearEarthObject(**row))
    except csv.Error as error:
        raise ValueError(f"Invalid CSV in '{neo_csv_path}': {error}") from error
    return neos


def load_approaches(cad_json_path: str | Path) -> list[CloseApproach]:
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    required_keys = ("fields", "data")
    required_fields = ("des", "cd", "dist", "v_rel")
    with open(cad_json_path, newline="", encoding="utf-8") as json_file:
        dataset = json.load(json_file)
    if not isinstance(dataset, dict):
        raise ValueError(
            f"Approach JSON '{cad_json_path}' must contain a top-level object"
        )
    if not all(key in dataset for key in required_keys):
        raise ValueError(
            f"Approach JSON '{cad_json_path}' must contain these keys: {', '.join(required_keys)}"
        )

    if not all(isinstance(dataset[key], list) for key in required_keys):
        raise ValueError(
            f"Approach JSON '{cad_json_path}' must use arrays for these keys: {', '.join(required_keys)}"
        )
    fields = dataset["fields"]
    if not all(isinstance(field, str) for field in fields):
        raise ValueError(
            f"Approach JSON '{cad_json_path}' every entry in fields must be of str type"
        )
    if not all(field in fields for field in required_fields):
        raise ValueError(
            f"Approach JSON '{cad_json_path}' must contain these fields:{', '.join(required_fields)}"
        )

    approaches: list[CloseApproach] = []
    fields = dataset["fields"]
    str_fields = ("des", "cd")
    numeric_fields = ("dist", "v_rel")
    for values in dataset["data"]:
        if not isinstance(values, list):
            raise ValueError(
                f"Approach JSON '{cad_json_path}' each data row must be an array"
            )

        if len(values) != len(fields):
            raise ValueError(
                f"Approach JSON '{cad_json_path}': row has {len(values)} values; "
                f"expected {len(fields)}."
            )
        info = dict(zip(fields, values, strict=True))
        if not all(
            isinstance(info[str_field], str) for str_field in str_fields
        ) or not all(
            isinstance(info[field], (str, int, float)) for field in numeric_fields
        ):
            raise ValueError(
                f"Approach JSON '{cad_json_path}': des and cd must be text; "
                "dist and v_rel must be numbers or numeric text."
            )
        approaches.append(CloseApproach(**info))
    return approaches
