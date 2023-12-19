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

# Ratings indices
proportionality: int = 0
competitiveness: int = 1
minority: int = 2
compactness: int = 3
splitting: int = 4


def main() -> None:
    args: argparse.Namespace = parse_args()

    scores: List[Dict[str, Any]] = read_scores(args.scores)
    metadata: Dict[str, Any] = read_json(args.metadata)

    output: Dict[str, Any] = {k: v for k, v in metadata.items() if k != "plans"}
    plans: List[Dict[str, Any]] = []
    notable_maps: List[Dict[str, Any]] = [{"map": "", "ratings": []} for _ in range(5)]

    total: int = 0
    qualifying: int = 0

    for plan in scores:
        total += 1
        ratings: List[int] = [int(x) for x in list(plan.values())[-5:]]
        if not qualifying_map(ratings):
            continue

        for dimension, current_best in enumerate(notable_maps):
            if better_map(ratings, current_best["ratings"], dimension):
                current_best["map"] = plan["map"]
                current_best["ratings"] = ratings

        qualifying += 1

    output["size"] = total
    output["qualifying"] = qualifying
    output["notable_maps"] = notable_maps

    write_json(args.notables, output)

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


def qualifying_map(ratings: List[int]) -> bool:
    if (
        ratings[proportionality] >= 20
        and ratings[competitiveness] >= 10
        and ratings[compactness] >= 20
        and ratings[splitting] >= 20
    ):
        return True
    else:
        return False


def better_map(ratings: List[int], current_best: List[int], dimension: int) -> bool:
    if (ratings[dimension] > current_best[dimension]) or (
        ratings[dimension] == current_best[dimension]
        and sum(ratings) > sum(current_best)
    ):
        return True
    else:
        return False


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
        "scores": "output/NC20C_RMfRST_100_scores.csv",
        "metadata": "output/NC20C_RMfRST_100_scores_metadata.json",
        "notables": "output/NC20C_RMfRST_100_notable_maps.json",
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
