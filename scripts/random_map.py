#!/usr/bin/env python3

"""
GENERATE A SINGLE RANDOM MAP BY CUTTING RANDOM SPANNING TREES

For example:

$ scripts/random_map.py \
--state NC \
--plantype lower \
--roughlyequal 0.10 \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--output temp/NC20L_random_plan.csv \
--log temp/NC20L_random_log.txt \
--no-debug

For documentation, type:

$ scripts/random_map.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict

import warnings

warnings.warn = lambda *args, **kwargs: None

from rdabase import (
    require_args,
    starting_seed,
    DISTRICTS_BY_STATE,
    write_json,
    load_data,
    load_graph,
    load_metadata,
    Assignment,
    write_csv,
)

from rdaensemble import gen_rmfrst_ensemble, make_plan


def main() -> None:
    args: argparse.Namespace = parse_args()

    data: Dict[str, Dict[str, int | str]] = load_data(args.data)
    graph: Dict[str, List[str]] = load_graph(args.graph)
    # metadata: Dict[str, Any] = load_metadata(args.state, args.data)

    N: int = DISTRICTS_BY_STATE[args.state][args.plantype]
    # N: int = int(metadata["D"]) <= Generalized for state houses
    seed: int = starting_seed(args.state, N) + args.offset

    with open(args.log, "w") as f:
        plans: List[Dict[str, str | float | Dict[str, int | str]]] = (
            gen_rmfrst_ensemble(
                1,
                seed,
                data,
                graph,
                N,
                f,
                roughly_equal=args.roughlyequal,
                verbose=args.verbose,
            )
        )

    plan_dict: Dict[str, int | str] = plans[0]["plan"]  # type: ignore
    assignments: List[Assignment] = make_plan(plan_dict)
    plan: List[Dict[str, str | int]] = [
        {"GEOID": a.geoid, "DISTRICT": a.district} for a in assignments
    ]

    write_csv(args.output, plan, ["GEOID", "DISTRICT"])


def parse_args():
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Generate a random maps."
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
    parser.add_argument("--offset", type=int, default=0, help="An offset for the seed")
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
        "--output",
        type=str,
        help="Plan CSV file",
    )
    parser.add_argument(
        "--roughlyequal",
        type=float,
        default=0.01,
        help="'Roughly equal' population threshold",
    )
    parser.add_argument(
        "--log",
        type=str,
        help="Log TXT file",
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
        # "plantype": "congress",
        "plantype": "lower",
        # "roughlyequal": 0.01,
        "roughlyequal": 0.10,
        "data": "../rdabase/data/NC/NC_2020_data.csv",
        "shapes": "../rdabase/data/NC/NC_2020_shapes_simplified.json",
        "graph": "../rdabase/data/NC/NC_2020_graph.json",
        # "output": "temp/NC20C_random_plan.csv",
        "output": "temp/NC20L_random_plan.csv",
        "log": "temp/NC20L_random_log.txt",
        "verbose": True,
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
