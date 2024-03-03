#!/usr/bin/env python3

"""
ADD PLANS TO AN ENSEMBLE

For example:

$ scripts/extend_ensemble.py \
--ensemble ../../iCloud/fileout/ensembles/NC20C_plans.json \
--plans ../../iCloud/fileout/hpc_batch/NC/pushed \
--no-debug

For documentation, type:

$ scripts/find_frontiers.py
"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict

from rdabase import require_args, read_json, write_json


def main() -> None:
    """Add plans to an ensemble."""

    args: argparse.Namespace = parse_args()

    ensemble: Dict[str, Any] = read_json(args.ensemble)
    plans: List[Dict[str, str | float | Dict[str, int | str]]] = ensemble["plans"]

    pass


def parse_args():
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Add the plans in a directory to an ensemble"
    )

    parser.add_argument(
        "--ensemble",
        type=str,
        help="The ensemble to extend",
    )
    parser.add_argument(
        "--plans",
        type=str,
        help="The directory with the CSV plans to add to it",
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
        "ensemble": "../../iCloud/fileout/ensembles/NC20C_plans.json",
        "plans": "../../iCloud/fileout/hpc_batch/NC/pushed",
        "verbose": True,
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
