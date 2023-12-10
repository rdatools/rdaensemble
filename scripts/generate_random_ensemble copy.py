#!/usr/bin/env python3

"""
GENERATE A COLLECTION OF RANDOM MAPS

For example:

$ scripts/generate_random_ensemble.py \
--state NC \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--size 1000 \
--plans output/NC_2020_random_maps_plans.json \
--log output/NC_2020_random_maps_log.txt \
--no-debug

For documentation, type:

$ scripts/generate_random_ensemble.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict, Tuple

from rdabase import (
    require_args,
    starting_seed,
    mkAdjacencies,
    populations,
    total_population,
    calc_population_deviation,
    Graph,
    Assignment,
    write_json,
)
from rdascore import load_data, load_graph, load_metadata

from rdaensemble import (
    random_map,
)


def main() -> None:
    args: argparse.Namespace = parse_args()

    data: Dict[str, Dict[str, int | str]] = load_data(args.data)
    graph: Dict[str, List[str]] = load_graph(args.graph)
    metadata: Dict[str, Any] = load_metadata(args.state, args.data)

    pairs: List[Tuple[str, str]] = mkAdjacencies(Graph(graph))

    pop_by_geoid: Dict[str, int] = populations(data)
    total_pop: int = total_population(pop_by_geoid)

    plans: List[Dict[str, str | float | Dict[str, int | str]]] = list()

    N: int = int(metadata["D"])
    start: int = starting_seed(args.state, N)
    seed: int = start
    conforming_count: int = 0

    with open(args.log, "a") as f:
        # TODO - Abstract this into a random_ensemble() function.
        while True:
            print(f"... {conforming_count} ...")
            print(f"Conforming count: {conforming_count}, random seed: {seed}", file=f)

            plan_name: str = f"{conforming_count:03d}_{seed}"

            try:
                # Generate a random contiguous & 'roughly' equal population partitioning of the state.
                assignments: List[Assignment] = random_map(
                    pairs,
                    pop_by_geoid,
                    N,
                    seed,
                )

                # Calculate the population deviation of the map.
                popdev: float = calc_population_deviation(
                    assignments, pop_by_geoid, total_pop, N
                )

                # If the map does not have 'roughly' equal population, discard it.
                if popdev > args.roughlyequal:
                    continue

                # Otherwise increment candidate count, save the plan, & score it.
                conforming_count += 1
                plan: Dict[str, int | str] = {a.geoid: a.district for a in assignments}
                plans.append({"name": plan_name, "plan": plan})  # No weights.

                # If the conforming candidate count equal to the number of iterations, stop.
                if conforming_count == args.size:
                    break

            except Exception as e:
                print(f"Failure: {e}", file=f)
                pass

            finally:
                seed += 1

        print(
            f"{conforming_count} conforming plans took {seed - start + 1} random seeds.",
            file=f,
        )

    write_json(args.plans, plans)


def parse_args():
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Generate a collection of random maps."
    )

    parser.add_argument(
        "--state",
        help="The two-character state code (e.g., NC)",
        type=str,
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
        "--size", type=int, default=1000, help="Number of maps to generate"
    )
    parser.add_argument(
        "--plans",
        type=str,
        help="Ensemble plans JSON file",
    )
    parser.add_argument(
        "--scores",
        type=str,
        help="Ensemble scores CSV file",
    )
    parser.add_argument(
        "--log",
        type=str,
        default="output/log.txt",
        help="Log TXT file",
    )
    parser.add_argument(
        "--roughlyequal",
        type=float,
        default=0.02,
        help="'Roughly equal' population threshold",
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
        "data": "../rdadata/data/NC/NC_2020_data.csv",
        "shapes": "../rdadata/data/NC/NC_2020_shapes_simplified.json",
        "graph": "../rdadata/data/NC/NC_2020_graph.json",
        "plans": "output/NC_2020_random_maps_plans.json",
        "size": 10,
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()
