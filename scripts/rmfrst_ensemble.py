#!/usr/bin/env python3

"""
GENERATE A COLLECTION OF RANDOM MAPS from RANDOM SPANNING TREES (RMfRST)

For example:

$ scripts/rmfrst_ensemble.py \
--state NC \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--size 1000 \
--plans output/NC20C_RMfRST_1000_plans.json \
--log output/NC20C_RMfRST_1000_log.txt \
--no-debug

For documentation, type:

$ scripts/rmfrst_ensemble.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict

from rdabase import (
    require_args,
    starting_seed,
    write_json,
)
from rdascore import load_data, load_graph, load_metadata

from rdaensemble import gen_rmfrst_ensemble, ensemble_metadata


def main() -> None:
    args: argparse.Namespace = parse_args()

    data: Dict[str, Dict[str, int | str]] = load_data(args.data)
    graph: Dict[str, List[str]] = load_graph(args.graph)
    metadata: Dict[str, Any] = load_metadata(args.state, args.data)

    N: int = int(metadata["D"])
    seed: int = starting_seed(args.state, N)

    ensemble: Dict[str, Any] = ensemble_metadata(
        xx=args.state,
        ndistricts=N,
        size=args.size,
        method="Random maps from random spanning trees (RMfRST)",
    )

    with open(args.log, "w") as f:
        plans: List[
            Dict[str, str | float | Dict[str, int | str]]
        ] = gen_rmfrst_ensemble(
            args.size, seed, data, graph, N, f, roughly_equal=args.roughlyequal
        )

    ensemble["plans"] = plans

    write_json(args.plans, ensemble)


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
        "--size", type=int, default=1000, help="Number of maps to generate"
    )
    parser.add_argument(
        "--plans",
        type=str,
        help="Ensemble plans JSON file",
    )
    parser.add_argument(
        "--scores",
        type=str,
        help="Ensemble scores CSV file",
    )
    parser.add_argument(
        "--log",
        type=str,
        help="Log TXT file",
    )
    parser.add_argument(
        "--roughlyequal",
        type=float,
        default=0.02,
        help="'Roughly equal' population threshold",
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
        "data": "../rdadata/data/NC/NC_2020_data.csv",
        "shapes": "../rdadata/data/NC/NC_2020_shapes_simplified.json",
        "graph": "../rdadata/data/NC/NC_2020_graph.json",
        "plans": "output/NC20C_RMfRST_1000_plans.json",
        "log": "output/NC20C_RMfRST_1000_log.json",
        "size": 10,
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()
