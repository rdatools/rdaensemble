#!/usr/bin/env python3

"""
MAKE AN ENSEMBLE FROM PRECINCT-ASSIGNMENT FILES FOR PLANS

For example:

$ scripts/make_ensemble_from_plans.py \
--state NC \
--plantype congress \
--csvdir ../../iCloud/fileout/tradeoffs/NC/ensembles/multiple-starts \
--pattern r"NC20C_start_\d{2}\.csv" \
--plans ../../iCloud/fileout/tradeoffs/NC/ensembles/multiple-starts/NC20C_plans_RANDOM.json \
--data ../rdabase/data/NC/NC_2020_data.csv \
--no-debug

For documentation, type:

$ scripts/make_ensemble_from_plans.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict

import os
import re
import warnings

warnings.warn = lambda *args, **kwargs: None

from rdabase import (
    require_args,
    read_csv,
    load_data,
    load_metadata,
    write_json,
)

from rdaensemble import ensemble_metadata


def main() -> None:
    args: argparse.Namespace = parse_args()

    #

    data: Dict[str, Dict[str, int | str]] = load_data(args.data)
    metadata: Dict[str, Any] = load_metadata(args.state, args.data, args.plantype)
    N: int = int(metadata["D"])

    csv_files: List[str] = get_matching_files(args.csvdir, args.pattern)

    ensemble: Dict[str, Any] = ensemble_metadata(
        xx=args.state,
        ndistricts=N,
        size=len(csv_files),
        method="From plans in CSV files",
    )
    # Update the type of plan (e.g., "congress", "upper", "lower"), based on the plantype arg
    ensemble["plan_type"] = args.plantype.title()
    ensemble["packed"] = False
    ensemble["plans"] = list()

    for csv_file in csv_files:
        csv_path: str = os.path.join(args.csvdir, csv_file)

        input_plan: List[Dict[str, Any]] = read_csv(csv_path, [str, int])
        assert "GEOID" in input_plan[0] or "GEOID20" in input_plan[0]
        assert "DISTRICT" in input_plan[0] or "District" in input_plan[0]
        geoid_field: str = "GEOID20" if "GEOID20" in input_plan[0] else "GEOID"
        district_field: str = "District" if "District" in input_plan[0] else "DISTRICT"
        assignments: Dict[str, int | str] = {
            str(row[geoid_field]): row[district_field] for row in input_plan
        }
        name: str = csv_file.split(".")[0]
        plan: Dict[str, Any] = {"name": name, "plan": assignments}
        ensemble["plans"].append(plan)

    if not args.debug:
        write_json(args.plans, ensemble)


def get_matching_files(dir: str, template: str) -> List[str]:
    """Get a list of filenames in a directory that match a given pattern.

    For example:
    get_matching_files("path/to/directory", r"NC20C_start_\d{2}\.csv")
    """
    # Compile the regular expression pattern
    pattern = re.compile(r"NC20C_start_\d{2}\.csv")

    # List to store matching filenames
    matching_files = []

    # Iterate through files in the directory
    for filename in os.listdir(dir):
        # Check if the filename matches the pattern
        if pattern.match(filename):
            matching_files.append(filename)

    return matching_files


def parse_args():
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Write a plan in an ensemble to a CSV."
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
        "--csvdir",
        type=str,
        help="The directory containing the CSV files",
    )
    parser.add_argument(
        "--pattern",
        type=str,
        help="The pattern to match the CSV files",
    )
    parser.add_argument(
        "--plans",
        type=str,
        help="The ensemble of plans to add it to",
    )

    parser.add_argument(
        "--data",
        type=str,
        help="Data file",
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
        "plantype": "congress",
        "csvdir": "../../iCloud/fileout/tradeoffs/NC/ensembles/multiple-starts",
        "pattern": r"NC20C_start_\d{2}\.csv",
        "plans": "../../iCloud/fileout/tradeoffs/NC/ensembles/multiple-starts/NC20C_random_plans.json",
        "data": "../rdabase/data/NC/NC_2020_data.csv",
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
