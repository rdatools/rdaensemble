#!/usr/bin/env python3

"""
FIND THE NOTABLE MAPS IN A SCORED ENSEMBLE OF MAPS

For example:

$ scripts/id_notable_maps.py \
--scores output/NC20C_RMfRST_1000_scores.csv \
--metadata output/NC20C_RMfRST_1000_scores_metadata.json \
--notables output/NC20C_RMfRST_1000_notables_maps.json \
--no-debug

For documentation, type:

$ scripts/id_notable_maps.py -h

NOTE - This is a work in progress not ready for use. 
       So far, maps split too many counties & aren't compact enough to be notable.
"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict

import csv

from rdabase import (
    require_args,
    read_json,
    write_json,
)


def main() -> None:
    args: argparse.Namespace = parse_args()

    scores: List[Dict[str, Any]] = read_scores(args.scores)
    metadata: Dict[str, Any] = read_json(args.metadata)

    output: Dict[str, Any] = {k: v for k, v in metadata.items() if k != "plans"}
    plans: List[Dict[str, Any]] = []
    proportionality = {"map": "", "ratings": []}
    competitiveness = {"map": "", "ratings": []}
    minority = {"map": "", "ratings": []}
    compactness = {"map": "", "ratings": []}
    splitting: Dict[str, Any] = {"map": "", "ratings": []}

    count = 0

    for plan in scores:
        if not (
            int(plan["proportionality"]) >= 20
            and int(plan["competitiveness"]) >= 10
            and int(plan["compactness"]) >= 20
            # and int(plan["splitting"]) >= 20 # NOTE: The maps split too many counties.
        ):
            continue

        count += 1

    print(f"Found {count} qualifying maps.")

    # Write notable maps (args.notables)
    # write_json(metadata_path, metadata)

    pass


def read_scores(input: str) -> List[Dict[str, Any]]:
    """Read the scores from a CSV file.

    map, ..., proportionality,competitiveness,minority,compactness,splitting
    """

    with open(input, "r") as f:
        scores: List[Dict[str, Any]] = []
        reader = csv.DictReader(f)
        for row in reader:
            scores.append(row)

        return scores


def parse_args():
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Generate a collection of random maps."
    )

    parser.add_argument(
        "--scores",
        type=str,
        help="Ensemble of scores in a CSV file",
    )
    parser.add_argument(
        "--metadata",
        type=str,
        help="Metadata JSON for the scoring CSV",
    )
    parser.add_argument(
        "--notables",
        type=str,
        help="Notable maps JSON file",
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    # Enable debug/explicit mode
    parser.add_argument("--debug", default=True, action="store_true", help="Debug mode")
    parser.add_argument(
        "--no-debug", dest="debug", action="store_false", help="Explicit mode"
    )

    args: Namespace = parser.parse_args()

    # Default values for args in debug mode
    debug_defaults: Dict[str, Any] = {
        "scores": "output/NC20C_RMfRST_1000_scores.csv",
        "metadata": "output/NC20C_RMfRST_1000_scores_metadata.json",
        "notables": "output/NC20C_RMfRST_1000_notable_maps.json",
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
