#!/usr/bin/env python3

"""
GENERATE AN ENSEMBLE OF MAPS using RECOM
by doing K chains of M steps each.

For example:

$ scripts/recom_ensemble_KxM.py \
--state NC \
--plantype congress \
--root ../tradeoffs/official_maps/NC_2022_Congress_Official_Proxy.csv \
--K 100 \
--M 100 \
--burnin 0 \
--data ../rdabase/data/NC/NC_2020_data.csv \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--plans ~/Downloads/NC20C_0100_0100_from_official.json \
--log ~/Downloads/NC20C_0100_0100_from_official_log.txt \
--no-debug

$ scripts/add_plan_to_ensemble.py \
--plan ../tradeoffs/official_maps/NC_2022_Congress_Official_Proxy.csv \
--plans ~/Downloads/NC20C_0100_0100_from_official.json \
--no-debug

$ scripts/score_ensemble.py \
--state NC \
--plans ~/Downloads/NC20C_0100_0100_from_official.json \
--data ../rdabase/data/NC/NC_2020_data.csv \
--eivotes ../tradeoffs/EI_estimates/NC_2020_est_votes.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--scores ~/Downloads/NC20C_0100_0100_from_official.csv \
--no-debug

$ scripts/recom_ensemble_KxM.py

For documentation, type:

$ scripts/recom_ensemble_KxM.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict

import random, os

import warnings

warnings.warn = lambda *args, **kwargs: None

from gerrychain.proposals import recom

from rdabase import (
    require_args,
    starting_seed,
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

    starting_plan: List[Dict[str, str | int]] = read_csv(args.start, [str, int])

    data: Dict[str, Dict[str, int | str]] = load_data(args.data)
    graph: Dict[str, List[str]] = load_graph(args.graph)
    metadata: Dict[str, Any] = load_metadata(args.state, args.data, args.plantype)

    N: int = int(metadata["D"])
    K: int = args.K  # Number of chains (starts)
    M: int = args.M  # Number of steps (mutations) per chain

    seed: int = starting_seed(args.state, N)
    random.seed(seed)

    ensemble: Dict[str, Any] = ensemble_metadata(
        xx=args.state,
        ndistricts=N,
        size=K * M,
        method="ReCom",
    )
    # Update the type of plan (e.g., "congress", "upper", "lower"), based on the plantype arg
    ensemble["plan_type"] = args.plantype.title()
    ensemble["packed"] = False
    plans: List[Dict[str, str | float | Dict[str, int | str]]] = []

    with open(args.log, "w") as f:
        for start in range(K):
            print(f"Starting Re-Com {start:04d} ...")
            print(f"Starting Re-Com {start:04d} ...", file=f)

            recom_graph, elections, back_map = prep_data(
                data, graph, initial_plan=starting_plan
            )

            chain = setup_unbiased_markov_chain(
                recom,
                M,
                recom_graph,
                elections,
                roughly_equal=args.roughlyequal,
                elasticity=args.elasticity,
                countyweight=args.countyweight,
                node_repeats=1,
                n_districts=N,
            )

            more_plans: List[Dict[str, str | float | Dict[str, int | str]]] = (
                run_unbiased_chain(
                    chain,
                    back_map,
                    f,
                    keep=M,
                )
            )

            for plan in more_plans:
                plan["name"] = f"{start:04d}.{plan['name']}"

            plans.extend(more_plans)

    file_name = os.path.basename(args.start)
    description: str = f"From: {file_name}, {K} starts each with {M} steps."
    ensemble["description"] = description
    ensemble["plans"] = plans
    if not args.debug:
        write_json(args.plans, ensemble)

    pass


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
        "--start",
        type=str,
        help="The starting plan",
    )
    parser.add_argument("--K", type=int, default=100, help="Number of chains (starts)")
    parser.add_argument(
        "--M", type=int, default=100, help="Number of steps (mutations) per chain"
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
        "start": "../tradeoffs/official_maps/NC_2022_Congress_Official_Proxy.csv",
        "K": 10,
        "M": 10,
        "data": "../rdabase/data/NC/NC_2020_data.csv",
        "graph": "../rdabase/data/NC/NC_2020_graph.json",
        "plans": "temp/NC20C_0010_0010_from_official.json",
        "log": "temp/NC20C_0010_0010_from_official_log.txt",
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
