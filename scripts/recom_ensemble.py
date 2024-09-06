#!/usr/bin/env python3

"""
GENERATE AN ENSEMBLE OF MAPS using RECOM

For example:

$ scripts/recom_ensemble.py \
--state NC \
--size 1000 \
--data ../rdabase/data/NC/NC_2020_data.csv \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--root ../tradeoffs/root_maps/NC20C_root_map.csv \
--plans ../../iCloud/fileout/ensembles/NC20C_plans.json \
--log ../../iCloud/fileout/ensembles/NC20C_log.txt \
--no-debug

$ scripts/recom_ensemble.py

For documentation, type:

$ scripts/recom_ensemble.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict

import random

import warnings

warnings.warn = lambda *args, **kwargs: None

from gerrychain.proposals import recom

from rdabase import (
    require_args,
    starting_seed,
    DISTRICTS_BY_STATE,
    read_csv,
    write_json,
    load_data,
    load_graph,
    load_metadata,
)
from rdaensemble import (
    ensemble_metadata,
    prep_data,
    setup_unbiased_markov_chain,
    run_unbiased_chain,
)


def main() -> None:
    """Generate an ensemble of maps using MCMC/ReCom."""

    args: argparse.Namespace = parse_args()

    data: Dict[str, Dict[str, int | str]] = load_data(args.data)
    graph: Dict[str, List[str]] = load_graph(args.graph)
    # metadata: Dict[str, Any] = load_metadata(args.state, args.data)

    root_plan: List[Dict[str, str | int]] = read_csv(args.root, [str, int])

    N: int = DISTRICTS_BY_STATE[args.state][args.plantype]
    # N: int = int(metadata["D"]) <= Generalized for state houses
    seed: int = starting_seed(args.state, N)

    ensemble: Dict[str, Any] = ensemble_metadata(
        xx=args.state,
        ndistricts=N,
        size=args.size,
        method="ReCom",
    )
    ensemble["packed"] = False

    with open(args.log, "w") as f:
        random.seed(seed)

        recom_graph, elections, back_map = prep_data(root_plan, data, graph)

        chain = setup_unbiased_markov_chain(
            recom,
            args.size,
            recom_graph,
            elections,
            roughly_equal=args.roughlyequal,
            elasticity=args.elasticity,
            countyweight=args.countyweight,
            node_repeats=1,
        )

        plans: List[Dict[str, str | float | Dict[str, int | str]]] = run_unbiased_chain(
            chain,
            # args.size,
            back_map,
            f,
        )

    ensemble["plans"] = plans
    if not args.debug:
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
        "--plantype",
        type=str,
        default="congress",
        help="The type of districts (congress, upper, lower)",
    )
    parser.add_argument(
        "--size", type=int, default=10, help="Number of maps to generate"
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
        default=0.01,
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
        "plantype": "congress",
        "data": "../rdabase/data/NC/NC_2020_data.csv",
        "graph": "../rdabase/data/NC/NC_2020_graph.json",
        "root": "../tradeoffs/root_maps/NC20C_root_map.csv",
        "plans": "temp/NC20C_plans.json",
        "log": "temp/NC20C_log.txt",
        "size": 10,
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
