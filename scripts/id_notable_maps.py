#!/usr/bin/env python3

"""
FIND THE NOTABLE MAPS IN A SCORED ENSEMBLE OF MAPS

For example:

$ scripts/id_notable_maps.py \
--scores ../../iCloud/fileout/ensembles/NC20C_scores_augmented.csv \
--metadata ../../iCloud/fileout/ensembles/NC20C_scores_augmented_metadata.json \
--notables ../../iCloud/fileout/ensembles/NC20C_notable_maps.json \
--no-debug

For documentation, type:

$ scripts/id_notable_maps.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict

import warnings

warnings.warn = lambda *args, **kwargs: None

import os, csv

from rdabase import (
    require_args,
    read_json,
    write_json,
)
from rdaensemble import id_notable_maps


def main() -> None:
    """Find the notable maps in a scored ensemble of maps."""

    args: argparse.Namespace = parse_args()

    scores: List[Dict[str, Any]] = read_scores(args.scores)
    metadata: Dict[str, Any] = read_json(args.metadata)

    filter: bool = not args.nofilter
    filters: List[int] = (
        [
            20,  # proportional
            10,  # competitive
            0,  # minority
            20,  # compact
            20,  # splitting,\
        ]
        if filter
        else [0, 0, 0, 0, 0]
    )

    output: Dict[str, Any] = metadata
    output["plans"] = os.path.basename(args.scores)
    notable_maps: Dict[str, Any] = id_notable_maps(scores, filters)
    output.update(notable_maps)

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
        "--nofilter", dest="nofilter", action="store_true", help="Don't filter plans"
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
        "scores": "../../iCloud/fileout/ensembles/NC20C_scores.csv",
        "metadata": "../../iCloud/fileout/ensembles/NC20C_scores_metadata.json",
        "notables": "../../iCloud/fileout/ensembles/NC20C_notable_maps.json",
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
