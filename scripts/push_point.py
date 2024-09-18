#!/usr/bin/env python3

"""
'PUSH' A POINT ON THE UNBIASED FRONTIER IN BOTH THE X & Y DIRECTIONS.

For documentation, type:

$ scripts/push_point.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict

import warnings

warnings.warn = lambda *args, **kwargs: None

from rdabase import require_args, read_json, write_json
from rdaensemble import ratings_dimensions, plan_from_ensemble


def main() -> None:
    """Make scatter plots for pairs of ratings dimensions for the plans in an unbiased ensemble and an optimized one."""

    args: argparse.Namespace = parse_args()

    #

    ensemble: Dict[str, Any] = read_json(args.plans)
    if "packed" in ensemble and ensemble["packed"] == True:
        raise Exception(f"Ensemble ({args.plans}) is packed. Unpack it first.")
    plans: List[Dict[str, Any]] = ensemble["plans"]

    data: Dict[str, Any] = read_json(args.frontier)
    frontiers: Dict[str, Any] = data["frontiers"]

    y_dim: str = args.ydim
    x_dim: str = args.xdim
    assert y_dim in ratings_dimensions and x_dim in ratings_dimensions

    index: int = args.index

    #

    pair: str = f"{y_dim}_{x_dim}"
    frontier: List[Dict[str, Any]] = frontiers[pair]
    plan_name: str = frontier[index]["map"]

    starting_plan: List[Dict[str, str | int]] = plan_from_ensemble(plan_name, ensemble)

    #

    print(f"Pushing {plan_name} on the unbiased frontier in the {y_dim} dimension ...")
    print(f"Pushing {plan_name} on the unbiased frontier in the {x_dim} dimension ...")

    print(f"Writing the pushed plans to {args.output} ...")

    pass  # TODO


def parse_args():
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Push a point on the unbiased frontier in both x & y directions."
    )

    parser.add_argument(
        "--plans",
        type=str,
        help="Ensemble of plans (JSON)",
    )
    parser.add_argument(
        "--frontier",
        type=str,
        help="Unbiased frontier (JSON)",
    )
    parser.add_argument(
        "--ydim",
        type=str,
        help="The y-axis dimension of the trade-off frontier (e.g., 'proportionality')",
    )
    parser.add_argument(
        "--xdim",
        type=str,
        help="The x-axis dimension of the trade-off frontier ' (e.g., 'compactness')",
    )
    parser.add_argument(
        "--index",
        type=int,
        help="The zero-based index of the pairwise frontier point to 'push'",
    )
    parser.add_argument(
        "--output",
        default="~/Downloads/",
        help="Path to output directory",
        type=str,
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
        "plans": "../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans.json",
        "frontier": "../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_frontiers.json",
        "ydim": "proportionality",
        "xdim": "competitiveness",
        "index": 5,
        "output": "intermediate/NC20C_plans_proportionality_competitiveness_5.json",
        "verbose": True,
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
