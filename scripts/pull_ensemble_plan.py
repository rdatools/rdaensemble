#!/usr/bin/env python3

"""
WRITE A PLAN IN AN ENSEMBLE TO A CSV

For example:

$ scripts/pull_ensemble_plan.py \
--plans ../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans.json \
--id 0000 \
--output temp/NC20C_plan_000.csv \
--no-debug

For documentation, type:

$ scripts/pull_ensemble_plan.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict

import warnings

warnings.warn = lambda *args, **kwargs: None

from rdabase import (
    require_args,
    Assignment,
    read_json,
    write_csv,
)

from rdaensemble import plan_from_ensemble, make_plan


def main() -> None:
    args: argparse.Namespace = parse_args()

    ensemble: Dict[str, Any] = read_json(args.plans)

    if "packed" in ensemble and ensemble["packed"] == True:
        raise Exception(f"Ensemble ({args.plans}) is packed. Unpack it first.")

    # TYPE HINT
    plan_item: Dict[str, str | float | Dict[str, int | str]] = plan_from_ensemble(
        args.id, ensemble
    )
    plan_dict: Dict[str, int | str] = plan_item["plan"]  # type: ignore
    assignments: List[Assignment] = make_plan(plan_dict)
    plan: List[Dict[str, str | int]] = [
        {"GEOID": a.geoid, "DISTRICT": a.district} for a in assignments
    ]

    write_csv(args.output, plan, ["GEOID", "DISTRICT"])


def parse_args():
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Write a plan in an ensemble to a CSV."
    )

    parser.add_argument(
        "--plans",
        type=str,
        help="Ensemble of plans",
    )
    parser.add_argument(
        "--id",
        type=str,
        help="The identifier of the plan to pull",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="The CSV file to write the plan to",
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
        "plans": "../../iCloud/fileout/tradeoffs/NC-alt/ensembles/NC20C_plans.json",
        "id": "1634",
        "output": "temp/NC20C_plan_1634.csv",
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
