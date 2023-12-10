#!/usr/bin/env python3

"""
SCORE AN ENSEMBLE OF MAPS

For example:

$ scripts/score_ensemble.py \
--state NC \
--plans output/NC_2020_random_maps_plans.json \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--scores output/NC_2020_random_maps_scores.csv \
--no-debug

For documentation, type:

$ scripts/score_ensemble.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
import json
from typing import Any, List, Dict

from rdabase import (
    require_args,
    write_csv,
)
from rdascore import load_data, load_shapes, load_graph, load_metadata, analyze_plan
from rdaensemble import score_ensemble


def main() -> None:
    args: argparse.Namespace = parse_args()

    data: Dict[str, Dict[str, int | str]] = load_data(args.data)
    shapes: Dict[str, Any] = load_shapes(args.shapes)
    graph: Dict[str, List[str]] = load_graph(args.graph)
    metadata: Dict[str, Any] = load_metadata(args.state, args.data)

    plans: List[Dict[str, str | float | Dict[str, int | str]]] = read_plans(args.plans)
    scores: List[Dict] = score_ensemble(plans, data, shapes, graph, metadata)

    fields: List[str] = list(scores[0].keys())
    write_csv(args.scores, scores, fields, precision="{:.6f}")


def read_plans(abs_path: str) -> List[Dict[str, str | float | Dict[str, int | str]]]:
    """Load a list of plans serialized in a JSON file."""

    try:
        with open(abs_path, "r") as f:
            return json.load(f)

    except:
        raise Exception("Exception reading JSON.")


def parse_args():
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Generate a collection of random maps."
    )

    parser.add_argument(
        "--state",
        help="The two-character state code (e.g., NC)",
        type=str,
    )
    parser.add_argument(
        "--plans",
        type=str,
        help="Ensemble of plans to score in a JSON file",
    )
    parser.add_argument(
        "--data",
        type=str,
        help="Data file",
    )
    parser.add_argument(
        "--shapes",
        type=str,
        help="Shapes abstract file",
    )
    parser.add_argument(
        "--graph",
        type=str,
        help="Graph file",
    )
    parser.add_argument(
        "--scores",
        type=str,
        help="Ensemble of resulting scores to a CSV file",
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
        "state": "NC",
        "plans": "output/NC_2020_random_maps_plans.json",
        "data": "../rdadata/data/NC/NC_2020_data.csv",
        "shapes": "../rdadata/data/NC/NC_2020_shapes_simplified.json",
        "graph": "../rdadata/data/NC/NC_2020_graph.json",
        "scores": "output/NC_2020_random_maps_scores.csv",
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()
