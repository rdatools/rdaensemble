#!/usr/bin/env python3

"""
SCORE AN ENSEMBLE OF MAPS

For example:

$ scripts/score_ensemble.py \
--state NC \
--plans ../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans.json \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--scores ../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_scores.csv \
--no-debug

For documentation, type:

$ scripts/score_ensemble.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict

import warnings

warnings.warn = lambda *args, **kwargs: None

from rdabase import (
    require_args,
    read_json,
    write_csv,
    write_json,
    load_data,
    load_shapes,
    load_graph,
    load_metadata,
    Assignment,
    load_plan,
)
from rdaensemble import score_ensemble, scores_metadata


def main() -> None:
    args: argparse.Namespace = parse_args()

    data: Dict[str, Dict[str, int | str]] = load_data(args.data)
    shapes: Dict[str, Any] = load_shapes(args.shapes)
    graph: Dict[str, List[str]] = load_graph(args.graph)
    metadata: Dict[str, Any] = load_metadata(args.state, args.data, args.plantype)

    # TYPE HINT
    # ensemble: Dict[str, Any] = read_json(args.plans)
    # plans: List[Dict[str, str | float | Dict[str, int | str]]] = ensemble["plans"]

    # if "packed" in ensemble and ensemble["packed"] == True:
    #     raise Exception(f"Ensemble ({args.plans}) is packed. Unpack it first.")

    sample_assignments: List[Assignment] = load_plan(args.plans)
    sample_plan: Dict[str, int | str] = {
        a.geoid: a.district for a in sample_assignments
    }
    plans: List[Dict[str, str | float | Dict[str, int | str]]] = [
        {"name": "ALARM_sample", "plan": sample_plan}
    ]

    alt_minority: bool = not args.no_alt_minority
    scores: List[Dict] = score_ensemble(
        plans, data, shapes, graph, metadata, alt_minority=alt_minority
    )

    metadata: Dict[str, Any] = scores_metadata(xx=args.state, plans=args.plans)
    metadata_path: str = args.scores.replace(".csv", "_metadata.json")

    fields: List[str] = list(scores[0].keys())
    write_csv(args.scores, scores, fields, precision="{:.4f}")

    write_json(metadata_path, metadata)


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
        "--plantype",
        type=str,
        default="congress",
        help="The type of districts (congress, upper, lower)",
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
        "-m",
        "--no-alt-minority",
        dest="no_alt_minority",
        action="store_true",
        help="No alt minority mode, i.e., use the DRA minority rating",
    )  # By default, use the alt minority rating
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
        "plantype": "congress",
        "plans": "../tradeoffs-dropbox/ALARM/NC_map_filtered.csv",
        # "plans": "../../iCloud/fileout/tradeoffs/NC/ensembles-upper/NC20C_plans.json",
        "data": "../rdabase/data/NC/NC_2020_data.csv",
        "shapes": "../rdabase/data/NC/NC_2020_shapes_simplified.json",
        "graph": "../rdabase/data/NC/NC_2020_graph.json",
        "scores": "temp/NC_map_filtered_scores.csv",
        # "scores": "temp/NC20U_plans.json",
        "verbose": True,
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
