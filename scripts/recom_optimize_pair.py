#!/usr/bin/env python3

"""
TODO - PAIRWISE OPTIMIZATION

Generate an ensemble of plans optimized for a *pair* of metrics using ReCom/single-metric optimization.

For example:
TODO - Update this example

$ scripts/recom_optimize_pair.py \
--state NC \
--size 10000 \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--plans ../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans_compactness_optimized.json \
--no-debug

$ scripts/recom_optimize_pair.py

For documentation, type:

$ scripts/recom_optimize_pair.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict, Callable

import random, os

import warnings

warnings.warn = lambda *args, **kwargs: None

from gerrychain.proposals import recom
from gerrychain.updaters import CountySplit

import rdapy as rda

from rdabase import (
    require_args,
    starting_seed,
    census_fields,
    Assignment,
    read_csv,
    write_json,
    load_data,
    load_shapes,
    load_graph,
    load_metadata,
    load_plan,
)
from rdascore import aggregate_data_by_district
from rdaensemble import (
    ensemble_metadata,
    prep_data,
    setup_optimized_markov_chain,
    run_optimized_chain,
    optimize_methods,
    ratings_dimensions,
    make_minority_proxy,
    optimization_metrics,
)


def main() -> None:
    """Generate an ensemble of maps optimized for a *pair* of metrics using ReCom/single-metric optimization."""

    args: argparse.Namespace = parse_args()

    method_label: str = args.method
    assert method_label in optimize_methods, f"Method '{method_label}' not found."
    method: Callable = optimize_methods[method_label]

    optimize_for: str = args.optimize
    optimize_dimensions: List[str] = optimize_for.split("_")
    for d in optimize_dimensions:
        assert d in ratings_dimensions, f"Optimize dimensionn '{d}' not found."

    # Read data in

    starting_plan: List[Dict[str, str | int]] = read_csv(args.root, [str, int])
    starting_assignments: List[Assignment] = load_plan(args.root)
    starting_name = os.path.splitext(os.path.basename(args.root))[0]

    print()
    print(f"Optimizing {starting_name} for ({', '.join(optimize_dimensions)}) ...")
    print()

    data: Dict[str, Dict[str, int | str]] = load_data(args.data)
    shapes: Dict[str, Any] = load_shapes(args.shapes)
    graph: Dict[str, List[str]] = load_graph(args.graph)
    metadata: Dict[str, Any] = load_metadata(args.state, args.data, args.plantype)

    # Aggregate statewide demographics for minority metric

    N: int = int(metadata["D"])
    n_districts: int = metadata["D"]
    n_counties: int = metadata["C"]
    county_to_index: Dict[str, int] = metadata["county_to_index"]
    district_to_index: Dict[int | str, int] = metadata["district_to_index"]

    aggregates: Dict[str, Any] = aggregate_data_by_district(
        starting_assignments,
        data,
        n_districts,
        n_counties,
        county_to_index,
        district_to_index,
    )
    statewide_demos: Dict[str, float] = dict()
    total_vap_field: str = census_fields[1]
    for demo in census_fields[2:]:  # Skip total population & total VAP
        simple_demo: str = demo.split("_")[0].lower()
        statewide_demos[simple_demo] = (
            aggregates["demos_totals"][demo]
            / aggregates["demos_totals"][total_vap_field]
        )

    # TODO - Make the metric optimization functions

    minority_proxy_fn: Callable[..., float] = make_minority_proxy(statewide_demos)
    optimization_metrics["minority"] = minority_proxy_fn

    # TODO - HERE
    metric: Callable = optimization_metrics["minority"]
    bigger_is_better: bool = True

    #

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

    y_dim = ratings_dimensions.index(optimize_dimensions[0]) + 1
    x_dim = ratings_dimensions.index(optimize_dimensions[1]) + 1
    prefix: str = f"{starting_name}_{y_dim}{x_dim}"

    # Setup and run the optimization chain

    recom_graph, elections, back_map = prep_data(
        data, graph, shapes, initial_plan=starting_plan
    )

    chain = setup_optimized_markov_chain(
        recom,
        recom_graph,
        elections,
        roughly_equal=args.roughlyequal,
        node_repeats=1,
        dimension=optimize_for,
        metric=metric,
        maximize=bigger_is_better,
    )

    more_plans: List[Dict[str, str | float | Dict[str, int | str]]] = (
        run_optimized_chain(
            chain,
            args.size,
            back_map,
            prefix,
            bigger_is_better=bigger_is_better,
            method=method,
        )
    )

    plans.extend(more_plans)

    print()
    print(
        f"Collected {len(more_plans)} plans optimized for ({', '.join(optimize_dimensions)})."
    )
    print()

    ensemble["plans"] = plans
    ensemble["size"] = len(plans)  # Not every optimization step is kept

    # TODO - Uncomment this to write the ensemble to a JSON file
    # if not args.debug:
    #     write_json(args.plans, ensemble)

    pass  # For debugging


def parse_args():
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Generate an ensemble of maps using MCMC/ReCom."
    )

    parser.add_argument(
        "--root",
        type=str,
        help="The plan (point) to optimize",
    )
    parser.add_argument(
        "--optimize",
        type=str,
        help="The *pair* of ratings dimension on which to optimize it, e.g., 'proportionality_compactness'",
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
        "--size",
        type=int,
        default=10,
        help="The number of optimization steps to perform",
    )
    parser.add_argument(
        "--plans",
        type=str,
        help="The resulting ensemble JSON file",
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
        "root": "../../iCloud/fileout/tradeoffs/NC/plans/NC20C_9417.csv",
        "optimize": "proportionality_minority",
        "state": "NC",
        "plantype": "congress",
        "size": 100,
        "plans": "temp/NC20C_9417_proportionality_compactness_plans.json",
        "data": "../rdabase/data/NC/NC_2020_data.csv",
        "shapes": "../rdabase/data/NC/NC_2020_shapes_simplified.json",
        "graph": "../rdabase/data/NC/NC_2020_graph.json",
        "method": "short_bursts",
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###


### END ###
