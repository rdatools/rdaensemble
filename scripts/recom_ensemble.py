#!/usr/bin/env python3

"""
GENERATE AN ENSEMBLE OF MAPS using RECOM

For example:

$ scripts/recom_ensemble.py \
--state NC \
--size 1000 \
--data ../rdabase/data/NC/NC_2020_data.csv \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--root ../../iCloud/fileout/rootmaps/NC20C_rootmap.csv \
--plans ../../iCloud/fileout/ensembles/NC20C_ReCom_1000_plans.json \
--log ../../iCloud/fileout/ensembles/NC20C_ReCom_1000_log.txt \
--no-debug

$ scripts/recom_ensemble.py

For documentation, type:

$ scripts/recom_ensemble.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict

from gerrychain.proposals import recom

from rdabase import (
    require_args,
    starting_seed,
    read_csv,
    write_json,
    load_data,
    # load_shapes,
    load_graph,
    load_metadata,
)
from rdaensemble import ensemble_metadata, gen_mcmc_ensemble


def main() -> None:
    """Generate an ensemble of maps using MCMC/ReCom."""

    args: argparse.Namespace = parse_args()

    data: Dict[str, Dict[str, int | str]] = load_data(args.data)
    # shapes: Dict[str, Any] = load_shapes(args.shapes)
    graph: Dict[str, List[str]] = load_graph(args.graph)
    metadata: Dict[str, Any] = load_metadata(args.state, args.data)

    root_plan: List[Dict[str, str | int]] = read_csv(args.root, [str, int])

    N: int = int(metadata["D"])
    seed: int = starting_seed(args.state, N)

    ensemble: Dict[str, Any] = ensemble_metadata(
        xx="NC",
        ndistricts=N,
        size=args.size,
        method="ReCom",
    )

    with open(args.log, "w") as f:
        plans: List[Dict[str, str | float | Dict[str, int | str]]] = gen_mcmc_ensemble(
            recom,
            args.size,
            root_plan,
            seed,
            data,
            graph,
            f,
            roughly_equal=args.roughlyequal,
            elasticity=args.elasticity,
            countyweight=args.countyweight,
            node_repeats=args.noderepeats,
            verbose=args.verbose,
        )

    ensemble["plans"] = plans

    write_json(args.plans, ensemble)


def parse_args():
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Generate an ensemble of maps using MCMC/ReCom."
    )

    parser.add_argument(
        "--state",
        help="The two-character state code (e.g., NC)",
        type=str,
    )
    parser.add_argument(
        "--size", type=int, default=1000, help="Number of maps to generate"
    )
    parser.add_argument(
        "--data",
        type=str,
        help="Data file",
    )
    parser.add_argument(
        "--graph",
        type=str,
        help="Graph file",
    )
    parser.add_argument(
        "--root",
        type=str,
        help="Root plan",
    )
    parser.add_argument(
        "--plans",
        type=str,
        help="Ensemble plans JSON file",
    )
    parser.add_argument(
        "--log",
        type=str,
        help="Log TXT file",
    )
    parser.add_argument(
        "--roughlyequal",
        type=float,
        default=0.02,
        help="'Roughly equal' population threshold",
    )
    parser.add_argument(
        "--elasticity",
        type=float,
        default=2.0,
        help="Allowable district boundary stretch factor",
    )
    parser.add_argument(
        "--countyweight",
        type=float,
        default=0.75,
        help="County weights",
    )
    parser.add_argument(
        "--noderepeats",
        type=int,
        default=1,
        help="How many different choices of root to use before drawing a new spanning tree.",
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
        "data": "../rdabase/data/NC/NC_2020_data.csv",
        "graph": "../rdabase/data/NC/NC_2020_graph.json",
        "root": "../../iCloud/fileout/rootmaps/NC20C_rootmap.csv",
        "plans": "../../iCloud/fileout/ensembles/NC20C_ReCom_10_plans.json",
        "log": "../../iCloud/fileout/ensembles/NC20C_ReCom_10_log.txt",
        "size": 10,
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###


### END ###
