#!/usr/bin/env python3

"""
GENERATE AN ENSEMBLE OF PLANS using RECOM and
OPTIMIZING for ONE RATINGS DIMENSION
USING ONE OF THREE OPTIMIZATION METHODS.

For example:

# TODO - Shapes
$ scripts/recom_optimized_ensemble.py \
--state NC \
--size 10000 \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--root ../tradeoffs/root_maps/NC20C_root_map.csv \
--plans ../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_sa_optimized_plans.json \
--log ../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_sa_optimized_log.txt \
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
from gerrychain.metrics.compactness import polsby_popper  # compute_polsby_popper

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
    setup_markov_chain,
    run_optimized_chain,
    simulated_annealing,
    short_bursts,
    tilted_runs,
)


# TODO - For debugging
# def polsby_popper(partition) -> Dict[int, float]:
#     """
#     Computes Polsby-Popper compactness scores for each district in the partition.

#     :param partition: The partition to compute scores for
#     :type partition: Partition

#     :returns: A dictionary mapping each district ID to its Polsby-Popper score
#     :rtype: Dict[int, float]
#     """
#     pass
#     return {
#         part: compute_polsby_popper(
#             partition["area"][part], partition["perimeter"][part]
#         )
#         for part in partition.parts
#     }


# TODO - Compactness
# https://gerrychain.readthedocs.io/en/latest/_modules/gerrychain/metrics/compactness/#
def average_polsby_popper(partition):
    """Estimate the compactness of a partition, using just Polsby-Popper."""

    n: int = len(partition)
    by_district: Dict[int, float] = partition["polsby_popper"]
    # by_district: Dict[int, float] = polsby_popper(partition)
    measurement: float = sum(by_district.values()) / n

    return measurement


# def average_polsby_popper(partition):
#     """Estimate the compactness of a partition, using just Polsby-Popper."""

#     n: int = len(partition)
#     by_district: Dict[int, float] = polsby_popper(partition)
#     measurement: float = sum(by_district.values()) / n

#     return measurement


def main() -> None:
    """Generate an ensemble of maps using MCMC/ReCom."""

    args: argparse.Namespace = parse_args()

    methods: Dict[str, Callable] = {
        "simulated_annealing": simulated_annealing,
        "short_bursts": short_bursts,
        "tilted_runs": tilted_runs,
    }
    label: str = args.method
    method: Callable = methods[label]

    # TODO - Paramaterize this
    metric: Callable
    num_cut_edges: Callable = lambda p: len(p["cut_edges"])  # Example

    metric = average_polsby_popper

    data: Dict[str, Dict[str, int | str]] = load_data(args.data)
    shapes: Dict[str, Any] = load_shapes(args.shapes)
    graph: Dict[str, List[str]] = load_graph(args.graph)
    metadata: Dict[str, Any] = load_metadata(args.state, args.data)

    root_plan: List[Dict[str, str | int]] = read_csv(args.root, [str, int])

    N: int = int(metadata["D"])
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

        recom_graph, elections, back_map = prep_data(root_plan, data, graph, shapes)

        chain = setup_markov_chain(
            recom,
            args.size,
            metric,
            recom_graph,
            elections,
            roughly_equal=args.roughlyequal,
            elasticity=args.elasticity,
            countyweight=args.countyweight,
            node_repeats=1,
        )

        plans: List[Dict[str, str | float | Dict[str, int | str]]] = (
            run_optimized_chain(
                chain,
                args.size,
                back_map,
                f,
                label=label,
                method=method,
                debug=args.debug,
            )
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
        "--method",
        type=str,
        default="simulated_annealing",
        help="A ReCom SingleMetricOptimizer optimization method",
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
        "root": "../tradeoffs/root_maps/NC20C_root_map.csv",
        "plans": "temp/NC20C_sa_optimized_plans.json",
        "log": "temp/NC20C_sa_optimized_log.txt",
        "size": 10,
        "method": "simulated_annealing",
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###


### END ###