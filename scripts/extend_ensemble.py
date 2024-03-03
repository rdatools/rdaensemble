#!/usr/bin/env python3

"""
ADD PLANS TO AN ENSEMBLE

For example:

$ scripts/extend_ensemble.py \
--ensemble ../../iCloud/fileout/ensembles/NC20C_plans.json \
--plans ../../iCloud/fileout/hpc_batch/NC/pushed \
--no-debug

For documentation, type:

$ scripts/extend_ensemble.py
"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict, TypeAlias

import os
from os import listdir
from os.path import isfile, join

from rdabase import require_args, read_json, read_csv, write_json

GeoID: TypeAlias = str
DistrictID: TypeAlias = int | str
Name: TypeAlias = str


def main() -> None:
    """Add plans to an ensemble."""

    args: argparse.Namespace = parse_args()

    existing_ensemble: Dict[str, Any] = read_json(args.input)
    plans: List[Dict[str, str | float | Dict[str, int | str]]] = existing_ensemble[
        "plans"
    ]
    print(f"# of plans in: {len(plans)}")

    extended_ensemble: Dict[str, Any] = {
        k: v for k, v in existing_ensemble.items() if k != "plans"
    }
    plan_files = [f for f in listdir(args.plans) if isfile(join(args.plans, f))]

    for p in plan_files:
        filename, file_extension = os.path.splitext(p)
        if file_extension == ".csv":
            plan_path: str = f"{args.plans}/{p}"
            assignments: List[Dict[str, str | int]] = read_csv(plan_path, [str, int])

            district_by_geoid: Dict[GeoID, DistrictID] = {
                str(a["GEOID"]): a["DISTRICT"] for a in assignments
            }
            name: str = "foo"  # TODO

            plan: Dict[str, Name | Dict[GeoID, DistrictID]] = {
                "name": name,
                "plan": district_by_geoid,
            }

            plans.append(plan)  # type: ignore

    extended_ensemble["plans"] = plans
    print(f"# of plans out: {len(plans)}")
    # TODO - Update time.

    write_json(args.output, extended_ensemble)

    pass


def parse_args():
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Add the plans in a directory to an ensemble"
    )

    parser.add_argument(
        "--input",
        type=str,
        help="An existing ensemble of plans",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="The extended ensemble of plans",
    )
    parser.add_argument(
        "--plans",
        type=str,
        help="The directory of plans to add to it",
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
        "input": "../../iCloud/fileout/ensembles/NC20C_plans.json",
        "output": "../../iCloud/fileout/ensembles/NC20C_plans_augmented.json",
        "plans": "../../iCloud/fileout/hpc_batch/NC/pushed",
        "verbose": True,
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
