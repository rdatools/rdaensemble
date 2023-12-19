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


metrics: List[str] = [
    "proportionality",
    "competitiveness",
    "minority",
    "compactness",
    "splitting",
]
dimensions: List[int] = list(range(5))


def main() -> None:
    """Find the notable maps in a scored ensemble of maps."""

    args: argparse.Namespace = parse_args()

    scores: List[Dict[str, Any]] = read_scores(args.scores)
    metadata: Dict[str, Any] = read_json(args.metadata)

    filters: List[int] = [
        args.proportional,
        args.competitive,
        args.minority,
        args.compact,
        args.splitting,
    ]

    output: Dict[str, Any] = metadata
    notable_maps: List[Dict[str, Any]] = [{m: "None", "ratings": []} for m in metrics]

    total: int = 0
    qualifying: int = 0

    for s in scores:
        total += 1
        ratings: List[int] = [int(s[m]) for m in metrics]
        if not qualifying_map(ratings, filters):
            continue

        for d in dimensions:
            if better_map(ratings, notable_maps[d], d):
                notable_maps[d][metrics[d]] = s["map"]
                notable_maps[d]["ratings"] = ratings

        qualifying += 1

    output["size"] = total
    output["filters"] = filters
    output["qualifying"] = qualifying
    output["plans"] = notable_maps

    write_json(args.notables, output)


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


def qualifying_map(ratings: List[int], filters: List[int]) -> bool:
    return all([ratings[i] >= filters[i] for i in dimensions])


def better_map(
    ratings: List[int], current_best: Dict[str, Any], dimension: int
) -> bool:
    if current_best[metrics[dimension]] == "None":
        return True
    if (ratings[dimension] > current_best["ratings"][dimension]) or (
        ratings[dimension] == current_best["ratings"][dimension]
        and sum(ratings) > sum(current_best["ratings"])
    ):
        return True
    else:
        return False


def parse_args():
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Find the notable maps in a scored ensemble of maps."
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
        "--proportional",
        type=int,
        default=20,
        help="Proportionality filter",
    )
    parser.add_argument(
        "--competitive",
        type=int,
        default=10,
        help="Competitiveness filter",
    )
    parser.add_argument(
        "--minority",
        type=int,
        default=0,
        help="Minority opportunity filter",
    )
    parser.add_argument(
        "--compact",
        type=int,
        default=20,
        help="Compactness filter",
    )
    parser.add_argument(
        "--splitting",
        type=int,
        default=20,
        help="County-district splitting filter",
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
        "scores": "output/NC20C_RMfRST_100_scores.csv",
        "metadata": "output/NC20C_RMfRST_100_scores_metadata.json",
        "notables": "output/NC20C_RMfRST_100_notable_maps.json",
        "splitting": 0,
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
