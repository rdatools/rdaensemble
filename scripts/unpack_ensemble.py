#!/usr/bin/env python3

"""
UNPACK ENSEMBLE PLANS

For example:

$ scripts/unpack_ensemble.py \
--input ~/Downloads/NC20C_plans_packed.json \
--output ~/Downloads/NC20C_plans.json \
--no-debug

For documentation, type:

$ scripts/unpack_ensemble.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from typing import List, Dict, Any, Optional, TypeAlias


from rdabase import (
    require_args,
    read_json,
    write_json,
)

GeoID: TypeAlias = str
DistrictID: TypeAlias = int | str

FeatureOffset: TypeAlias = int
DistrictOffset: TypeAlias = int

Name: TypeAlias = str
Weight: TypeAlias = float


def main() -> None:
    """Unpack the plans of a packed ensemble."""

    args: argparse.Namespace = parse_args()

    packed_ensemble: Dict[str, Any] = read_json(args.input)
    packed_plans: List[Dict[str, Name | Weight | Dict[GeoID, DistrictID]]] = (
        packed_ensemble["plans"]
    )

    unpacked_ensemble: Dict[str, Any] = {
        k: v for k, v in packed_ensemble.items() if k != "plans"
    }
    unpacked_ensemble["packed"] = False
    unpacked_plans: List[Dict[str, Name | Weight | Dict[GeoID, DistrictID]]] = []
    unpacked_plans.append(packed_plans[0])

    prev: Dict[GeoID, DistrictID] = packed_plans[0]["plan"]  # type: ignore

    for packed_plan in packed_plans[1:]:
        name: str = packed_plan["name"]  # type: ignore
        weight: Optional[float] = (
            packed_plan["weight"] if "weight" in packed_plan else None
        )  # type: ignore
        delta: Dict[GeoID, DistrictID] = packed_plan["plan"]  # type: ignore

        prev.update(delta)
        next: Dict[GeoID, DistrictID] = dict(prev)

        unpacked_plan: Dict[str, Name | Weight | Dict[GeoID, DistrictID]] = (
            {"name": name, "weight": weight, "plan": next}
            if weight is not None
            else {"name": name, "plan": next}
        )
        unpacked_plans.append(unpacked_plan)

    unpacked_ensemble["plans"] = unpacked_plans

    write_json(args.output, unpacked_ensemble)


def parse_args():
    parser: ArgumentParser = argparse.ArgumentParser(description="Parse arguments.")

    parser.add_argument(
        "--input",
        type=str,
        help="An unpacked ensemble of plans",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="The equivalent packed ensemble of plans",
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
        "input": "/ensembles/NC20C_plans_packed.json",
        "output": "~/Downloads/NC20C_plans.json",
        "verbose": True,
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
