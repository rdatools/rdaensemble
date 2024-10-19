#!/usr/bin/env python3

"""
GENERATE AN ENSEMBLE OF MAPS using RECOM

For example:

$ scripts/recom_ensemble.py \
--state NC \
--plantype congress \
--keep 10000 \
--start random_maps/NC20C_random_plan.csv \
--roughlyequal 0.01 \
--data ../rdabase/data/NC/NC_2020_data.csv \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--plans ../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans.json \
--log ../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_log.txt \
--no-debug

$ scripts/recom_ensemble.py \
--state NC \
--plantype congress \
--keep 10000 \
--start random_maps/NC20C_random_plan.csv \
--nocompactnesslimit \
--roughlyequal 0.01 \
--data ../rdabase/data/NC/NC_2020_data.csv \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--plans ../../iCloud/fileout/tradeoffs/NC/ensembles/minimal-constraints/NC20C_plans_MINIMALLY_CONSTRAINED.json \
--log ../../iCloud/fileout/tradeoffs/NC/ensembles/minimal-constraints/NC20C_log_MINIMALLY_CONSTRAINED.txt \
--no-debug

$ scripts/recom_ensemble.py \
--state NC \
--plantype congress \
--keep 10000 \
--start random_maps/NC20C_random_plan.csv \
--wilson \
--roughlyequal 0.01 \
--data ../rdabase/data/NC/NC_2020_data.csv \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--plans ../../iCloud/fileout/tradeoffs/NC/ensembles/spanning-tree/NC20C_plans_WILSON.json \
--log ../../iCloud/fileout/tradeoffs/NC/ensembles/spanning-tree/NC20C_log_WILSON.txt \
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

    assert (
        args.random_start or args.start
    ), "Must specify either --randomstart or --root"
    assert not (
        args.random_start and args.start
    ), "Cannot specify both --randomstart and --root"

    assert (
        args.sample == 0 or not args.unique
    ), "Cannot use --sample and --unique modes at the same time"

    max_chain_length: int = 10 ^ 6
    chain_length: int = (
        max_chain_length
        if args.unique
        else args.burnin + (args.keep * max(1, args.sample))
    )

    bound_compactness: bool = not args.no_compactness_limit

    description: str = (
        f"Burn-in: {args.burnin}, Keep: {args.keep}, Sample: {args.sample}, Unique: {args.unique}, Compactness bounded: {bound_compactness}, Wilson: {args.wilson_sampling}"
    )
    print(f"ReCom: {description}")

    #

    starting_plan: List[Dict[str, str | int]] = []
    if args.start:
        starting_plan = read_csv(args.start, [str, int])

    data: Dict[str, Dict[str, int | str]] = load_data(args.data)
    graph: Dict[str, List[str]] = load_graph(args.graph)
    metadata: Dict[str, Any] = load_metadata(args.state, args.data, args.plantype)

    N: int = int(metadata["D"])
    seed: int = starting_seed(args.state, N)
    random.seed(seed)

    ensemble: Dict[str, Any] = ensemble_metadata(
        xx=args.state,
        ndistricts=N,
        size=args.keep,
        method="ReCom",
    )
    # Update the type of plan (e.g., "congress", "upper", "lower"), based on the plantype arg
    ensemble["plan_type"] = args.plantype.title()
    ensemble["packed"] = False

    with open(args.log, "w") as f:
        recom_graph, elections, back_map = None, None, None
        if args.random_start:
            recom_graph, elections, back_map = prep_data(data, graph)
        else:
            recom_graph, elections, back_map = prep_data(
                data, graph, initial_plan=starting_plan
            )

        chain = setup_unbiased_markov_chain(
            recom,
            chain_length,
            recom_graph,
            elections,
            roughly_equal=args.roughlyequal,
            elasticity=args.elasticity,
            countyweight=args.countyweight,
            node_repeats=1,
            n_districts=N,
            random_start=args.random_start,
            bound_compactness=bound_compactness,
            wilson_sampling=args.wilson_sampling,
        )

        plans: List[Dict[str, str | float | Dict[str, int | str]]] = run_unbiased_chain(
            chain,
            back_map,
            f,
            random_start=args.random_start,
            burn_in=args.burnin,
            keep=args.keep,
            sample=args.sample,
            unique=args.unique,
        )

    ensemble["description"] = description
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
        "--burnin",
        type=int,
        default=0,
        help="The number of plans to skip before starting to collect them",
    )
    parser.add_argument(
        "--keep", type=int, default=10000, help="The number of plans to keep"
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=0,
        help="How frequently to sample plans",
    )
    parser.add_argument(
        "--unique", dest="unique", action="store_true", help="Unique districts mode"
    )
    parser.add_argument(
        "--start",
        type=str,
        help="The starting plan",
    )
    parser.add_argument(
        "--randomstart",
        dest="random_start",
        action="store_true",
        help="Start with random assignments",
    )
    parser.add_argument(
        "--wilson",
        dest="wilson_sampling",
        action="store_true",
        help="Wilson sampling mode",
    )

    parser.add_argument(
        "--nocompactnesslimit",
        dest="no_compactness_limit",
        action="store_true",
        help="Don't bound compactness",
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
        "keep": 10,
        "start": "random_maps/NC20C_random_plan.csv",
        "wilson_sampling": True,
        # "random_start": True,
        "data": "../rdabase/data/NC/NC_2020_data.csv",
        "graph": "../rdabase/data/NC/NC_2020_graph.json",
        "plans": "temp/NC20C_plans_TEST.json",
        "log": "temp/NC20C_log_TEST.txt",
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
