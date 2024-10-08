#!/usr/bin/env python3

"""
WRITE A PLAN IN AN ENSEMBLE TO A CSV

For example:

$ scripts/add_plan_to_ensemble.py \
--plan ../tradeoffs/official_maps/NC_2022_Congress_Official_Proxy.csv \
--plans ../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans.json \
--name official-proxy \
--no-debug

For documentation, type:

$ scripts/pull_plan_from_ensemble.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict

import warnings

warnings.warn = lambda *args, **kwargs: None

from rdabase import (
    require_args,
    read_csv,
    read_json,
    write_json,
)

from rdaensemble import plan_from_ensemble, make_plan


def main() -> None:
    args: argparse.Namespace = parse_args()

    #

    ensemble: Dict[str, Any] = read_json(args.plans)

    if "packed" in ensemble and ensemble["packed"] == True:
        raise Exception(f"Ensemble ({args.plans}) is packed. Unpack it first.")

    input_plan: List[Dict[str, Any]] = read_csv(args.plan, [str, int])
    assert "GEOID" in input_plan[0] or "GEOID20" in input_plan[0]
    assert "DISTRICT" in input_plan[0] or "District" in input_plan[0]
    geoid_field: str = "GEOID20" if "GEOID20" in input_plan[0] else "GEOID"
    district_field: str = "District" if "District" in input_plan[0] else "DISTRICT"
    assignments: Dict[str, int | str] = {
        str(row[geoid_field]): row[district_field] for row in input_plan
    }
    plan: Dict[str, Any] = {"name": args.name, "plan": assignments}

    ensemble["plans"] = [plan] + ensemble["plans"]
    ensemble["size"] += 1

    if not args.debug:
        write_json(args.plans, ensemble)


def parse_args():
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Write a plan in an ensemble to a CSV."
    )

    parser.add_argument(
        "--plan",
        type=str,
        help="The path to the plan to add",
    )
    parser.add_argument(
        "--plans",
        type=str,
        help="The ensemble of plans to add it to",
    )
    parser.add_argument(
        "--name",
        type=str,
        help="The name to give the plan in the ensemble",
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
        "plan": "../tradeoffs/official_maps/NC_2022_Congress_Official_Proxy.csv",
        "plans": "temp/NC20C_plans.json",
        "name": "official-proxy",
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
