#!/usr/bin/env python3

"""
PACK ENSEMBLE PLANS

For example:

$ scripts/pack_ensemble.py \
--input ../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans.json \
--output ~/Downloads/NC20C_plans_packed.json \
--no-debug

For documentation, type:

$ scripts/pack_ensemble.py -h

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
    """Pack the plans of an ensemble to reduce the size on disk.

    NOTE - Packing depends on successive plans being mutations of previous plans!
    """

    args: argparse.Namespace = parse_args()

    ensemble: Dict[str, Any] = read_json(args.input)
    plans: List[Dict[str, Name | Weight | Dict[GeoID, DistrictID]]] = ensemble["plans"]

    packed_ensemble: Dict[str, Any] = {
        k: v for k, v in ensemble.items() if k != "plans"
    }
    packed_ensemble["packed"] = True
    packed_plans: List[Dict[str, Name | Weight | Dict[GeoID, DistrictID]]] = []
    packed_plans.append(plans[0])

    prev: Dict[GeoID, DistrictID] = plans[0]["plan"]  # type: ignore

    for unpacked_plan in plans[1:]:
        name: str = unpacked_plan["name"]  # type: ignore
        weight: Optional[float] = (
            unpacked_plan["weight"] if "weight" in unpacked_plan else None
        )  # type: ignore
        next: Dict[GeoID, DistrictID] = unpacked_plan["plan"]  # type: ignore

        delta: Dict[GeoID, DistrictID] = {
            k: next[k] for k in next if next[k] != prev[k]
        }  # Assumes that the set of keys are the same
        packed_plan: Dict[str, Name | Weight | Dict[GeoID, DistrictID]] = (
            {"name": name, "weight": weight, "plan": delta}
            if weight is not None
            else {"name": name, "plan": delta}
        )

        packed_plans.append(packed_plan)
        prev = next

    packed_ensemble["plans"] = packed_plans

    write_json(args.output, packed_ensemble)


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
        "input": "../../iCloud/fileout/ensembles/NC20C_plans.json",
        "output": "~/Downloads/NC20C_plans_packed.json",
        "verbose": True,
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
