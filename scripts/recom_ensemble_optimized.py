#!/usr/bin/env python3

"""
GENERATE AN ENSEMBLE OF PLANS using RECOM and
OPTIMIZING for ONE RATINGS DIMENSION
USING ONE OF THREE OPTIMIZATION METHODS.

For example:

$ scripts/recom_ensemble_optimized.py \
--state NC \
--size 10000 \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--plans ../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans_compactness_optimized.json \
--no-debug

$ scripts/recom_ensemble.py

For documentation, type:

$ scripts/recom_ensemble.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict, Callable

import random

import warnings

warnings.warn = lambda *args, **kwargs: None

from gerrychain.proposals import recom

import rdapy as rda

from rdabase import (
    require_args,
    starting_seed,
    read_csv,
    write_json,
    load_data,
    load_shapes,
    load_graph,
    load_metadata,
)
from rdaensemble import (
    ensemble_metadata,
    prep_data,
    setup_optimized_markov_chain,
    run_optimized_chain,
    simulated_annealing,
    short_bursts,
    tilted_runs,
)

num_cut_edges: Callable = lambda p: len(p["cut_edges"])


def average_polsby_popper(partition):
    """Estimate the compactness of a partition, using just Polsby-Popper."""

    measurement: float = sum(partition["polsby-popper"].values()) / len(partition)

    return measurement


def proportionality_proxy(partition):
    """Use the EG of a partition as a proxy for disproportionality."""

    eg: float = abs(partition["election_composite"].efficiency_gap())

    return eg


def competitiveness(partition):
    """Estimate the competitiveness of a partition."""

    Vf_array: List[float] = partition["election_composite"].percents("Democratic")

    cD: float = rda.est_competitive_districts(Vf_array)

    return cD


def main() -> None:
    """Generate an ensemble of maps using MCMC/ReCom."""

    args: argparse.Namespace = parse_args()

    optimize_methods: Dict[str, Callable] = {
        "simulated_annealing": simulated_annealing,
        "short_bursts": short_bursts,
        "tilted_runs": tilted_runs,
    }
    method_label: str = args.method
    assert method_label in optimize_methods, f"Method '{method_label}' not found."
    method: Callable = optimize_methods[method_label]

    optimize_options: List[str] = [
        "proportionality",
        "competitiveness",
        "minority",
        "compactness",
        "splitting",
    ]
    option: str = args.optimize
    assert option in optimize_options, f"Optimize dimensionn '{option}' not found."
    assert option in [
        "proportionality",
        "competitiveness",
        "compactness",
    ], f"Optimize dimension '{option}' not implemented."
    optimize_for: str = option

    # TODO - Hard-coded to Notable Map CSV files. Parameterize this.
    plan_dimensions: List[str] = [
        "proportional",
        "competitive",
        "minority",
        "compact",
        "splitting",
    ]
    starting_dir: str = f"../tradeoffs/notable_maps/{args.state}/"
    starting_plan_paths: List[str] = [
        f"{args.state}_2022_Congress_{dim.capitalize()}_NOSPLITS.csv"
        for dim in plan_dimensions
    ]

    # End parameterization

    metrics: Dict[str, Any] = {
        "proportionality": {"metric": proportionality_proxy, "bigger_is_better": False},
        "competitiveness": {"metric": competitiveness, "bigger_is_better": True},
        "compactness": {"metric": average_polsby_popper, "bigger_is_better": True},
        # TODO - Add other metrics
    }
    metric: Callable = metrics[optimize_for]["metric"]
    bigger_is_better: bool = metrics[optimize_for]["bigger_is_better"]

    steps: int = round(args.size / len(starting_plan_paths))

    data: Dict[str, Dict[str, int | str]] = load_data(args.data)
    shapes: Dict[str, Any] = load_shapes(args.shapes)
    graph: Dict[str, List[str]] = load_graph(args.graph)
    metadata: Dict[str, Any] = load_metadata(args.state, args.data)

    N: int = int(metadata["D"])
    seed: int = starting_seed(args.state, N)
    random.seed(seed)

    ensemble: Dict[str, Any] = ensemble_metadata(
        xx=args.state,
        ndistricts=N,
        size=args.size,  # Update this below
        method="ReCom-Optimized",
    )
    ensemble["packed"] = False

    plans: List[Dict[str, str | float | Dict[str, int | str]]] = []

    print()
    print(
        f"Optimizing plans for {optimize_for} using {' '.join(method_label.split('_'))}."
    )
    print()

    for j, starting_plan_path in enumerate(starting_plan_paths):
        print()
        print(f"Starting plan: {starting_plan_path}")
        print()

        prefix: str = (
            f"{list(optimize_methods.keys()).index(args.method) + 1}{optimize_options.index(optimize_for) + 1}{j + 1}"
        )

        plan_path: str = starting_dir + starting_plan_path

        starting_plan: List[Dict[str, str | int]] = read_csv(plan_path, [str, int])
        recom_graph, elections, back_map = prep_data(starting_plan, data, graph, shapes)

        chain = setup_optimized_markov_chain(
            recom,
            recom_graph,
            elections,
            roughly_equal=args.roughlyequal,
            node_repeats=1,
            metric=metric,
            maximize=bigger_is_better,
        )

        more_plans: List[Dict[str, str | float | Dict[str, int | str]]] = (
            run_optimized_chain(
                chain,
                steps,
                back_map,
                prefix,
                bigger_is_better=bigger_is_better,
                method=method,
            )
        )

        plans.extend(more_plans)

        print()
        print(f"Collected {len(more_plans)} plans optimized for {optimize_for}.")
        print()

    ensemble["plans"] = plans
    ensemble["size"] = len(plans)  # Not every optimization step is kept

    print()
    print(f"Collected {len(plans)} plans optimized for {optimize_for}.")
    print()

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
        "--size", type=int, default=10, help="Number of maps to generate"
    )
    parser.add_argument(
        "--data",
        type=str,
        help="Data file",
    )
    parser.add_argument(
        "--shapes",
        type=str,
        help="Shapes abstract file",
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
        "--roughlyequal",
        type=float,
        default=0.01,
        help="'Roughly equal' population threshold",
    )
    parser.add_argument(
        "--method",
        type=str,
        default="short_bursts",
        help="A ReCom SingleMetricOptimizer optimization method",
    )
    parser.add_argument(
        "--optimize",
        type=str,
        help="The ratings dimension on which to optimize",
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
        "shapes": "../rdabase/data/NC/NC_2020_shapes_simplified.json",
        "graph": "../rdabase/data/NC/NC_2020_graph.json",
        "plans": "temp/NC20C_sa_optimized_plans.json",
        "size": 100,
        "method": "short_bursts",
        "optimize": "competitiveness",
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###


### END ###
