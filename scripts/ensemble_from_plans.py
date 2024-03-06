#!/usr/bin/env python3

"""
MAKE AN ENSEMBLE FROM A DIRECTORY OF PLAN CSVs
created from a base ensemble, e.g., by pushing

For example:

$ scripts/ensemble_from_plans.py \
--base ../../iCloud/fileout/ensembles/NC20C_plans.json \
--plans ../../iCloud/fileout/ensembles/NC20C_plans_pushed.json \
--dir ../../iCloud/fileout/hpc_dropbox/NC/pushed \
--no-debug

For documentation, type:

$ scripts/ensemble_from_plans.py

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict, TypeAlias

import os
from os import listdir
from os.path import isfile, join
import datetime

from rdabase import require_args, read_json, read_csv, write_json

GeoID: TypeAlias = str
DistrictID: TypeAlias = int | str
Name: TypeAlias = str


def main() -> None:
    """Make an ensemble from a directory of plans."""

    args: argparse.Namespace = parse_args()

    existing_ensemble: Dict[str, Any] = read_json(args.base)
    plans: List[Dict[str, str | float | Dict[str, int | str]]] = []
    # = existing_ensemble["plans"]

    new_ensemble: Dict[str, Any] = {
        k: v for k, v in existing_ensemble.items() if k != "plans"
    }
    plan_files = [f for f in listdir(args.dir) if isfile(join(args.dir, f))]

    for p in plan_files:
        filename, file_extension = os.path.splitext(p)
        if file_extension == ".csv":
            plan_path: str = f"{args.dir}/{p}"
            assignments: List[Dict[str, str | int]] = read_csv(plan_path, [str, int])

            district_by_geoid: Dict[GeoID, DistrictID] = {
                str(a["GEOID"]): a["DISTRICT"] for a in assignments
            }
            root: str = "_".join(filename.split("_")[1:-1])
            name: str = f"X_{root}"

            plan: Dict[str, Name | Dict[GeoID, DistrictID]] = {
                "name": name,
                "plan": district_by_geoid,
            }

            plans.append(plan)  # type: ignore

    new_ensemble["plans"] = plans

    new_ensemble["size"] = len(plans)
    new_ensemble["method"] = f"{existing_ensemble['method']}, pushed"
    timestamp = datetime.datetime.now()
    new_ensemble["date_created"] = timestamp.strftime("%x")
    new_ensemble["time_created"] = timestamp.strftime("%X")

    write_json(args.plans, new_ensemble)

    pass


def parse_args():
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Add the plans in a directory to an ensemble"
    )

    parser.add_argument(
        "--base",
        type=str,
        help="An existing ensemble of plans",
    )
    parser.add_argument(
        "--plans",
        type=str,
        help="The extended ensemble of plans",
    )
    parser.add_argument(
        "--dir",
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
        "base": "../../iCloud/fileout/ensembles/NC20C_plans.json",
        "plans": "../../iCloud/fileout/ensembles/NC20C_plans_augmented.json",
        "dir": "../../iCloud/fileout/hpc_batch/NC/pushed",
        "verbose": True,
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
