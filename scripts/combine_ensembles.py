#!/usr/bin/env python3

"""
COMBINE THE PLANS FROM MULTIPLE ENSEMBLES

For example:

$ scripts/combine_ensembles.py \
--ensembles ../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans_optimized_proportionality.json \
            ../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans_optimized_competitiveness.json \
            ../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans_optimized_minority.json \
            ../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans_optimized_compactness.json \
            ../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans_optimized_splitting.json \
--output ../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans_optimized.json \
--no-debug

For documentation, type:

$ scripts/combine_ensembles.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict

import warnings

warnings.warn = lambda *args, **kwargs: None

from rdabase import (
    require_args,
    read_json,
    write_json,
)

from rdaensemble import ensemble_metadata


def main() -> None:
    args: argparse.Namespace = parse_args()

    ensemble_files: List[str] = (
        args.ensembles
        if isinstance(args.ensembles, list)
        else args.ensembles.split(",")
    )

    print(f"Ensembles to combine:")
    for e in ensemble_files:
        print(f"- {e}")

    combined_ensemble: Dict[str, Any] = {}
    combined_ensemble["packed"] = False
    combined_ensemble["method"] = "Combining multiple independently generated ensembles"

    plans: List[Dict[str, str | float | Dict[str, int | str]]] = []
    total_size: int = 0

    for i, e in enumerate(ensemble_files):
        ensemble: Dict[str, Any] = read_json(e)

        if "packed" in ensemble and ensemble["packed"] == True:
            raise Exception(f"Ensemble ({e}) is packed. Unpack it first.")

        print(f"Ensemble {e} has {len(ensemble['plans'])} plans.")
        total_size += len(ensemble["plans"])
        if len(ensemble["plans"]) > 0:
            plans.extend(ensemble["plans"])

    combined_ensemble["size"] = total_size
    combined_ensemble["plans"] = plans

    if not args.debug:
        write_json(args.output, combined_ensemble)


# def list_of_strings(arg):
#     return arg.split(" ")


def parse_args():
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Combine the plans from multiple ensembles."
    )

    parser.add_argument(
        "-e", "--ensembles", help="List of ensembles to combine", type=str, nargs="+"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="The JSON file to write the combined ensemble to",
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
        "ensembles": [
            "../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans_optimized_proportionality.json",
            "../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans_optimized_competitiveness.json",
            "../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans_optimized_minority.json",
            "../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans_optimized_compactness.json",
            "../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans_optimized_splitting.json",
        ],
        "output": "temp/NC20C_plans_combined.csv",
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
