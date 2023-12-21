#!/usr/bin/env python3

"""
GENERATE AN ENSEMBLE OF MAPS using RECOM

For example:

$ scripts/recom_ensemble.py \
--state NC \
--data ../rdabase/data/NC/NC_2020_data.csv \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--root ../rdaroot/output/NC20C_RMfRST_100_rootmap.csv \
--size 1000 \
--plans ensembles/NC20C_ReCom_1000_plans.json \
--log ensembles/NC20C_ReCom_1000_log.txt \
--no-debug

For documentation, type:

$ scripts/recom_ensemble.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict, Tuple

from functools import partial

# import networkx as nx
from gerrychain import (
    GeographicPartition,
    Partition,
    Graph,
    MarkovChain,
    proposals,
    updaters,
    constraints,
    accept,
    Election,
)
from gerrychain.updaters import Tally, cut_edges
from gerrychain.proposals import recom
from gerrychain.partition.assignment import Assignment

from rdabase import (
    require_args,
    Graph as RDAGraph,
    mkAdjacencies,
    read_csv,
    read_json,
    write_csv,
    write_json,
)
from rdascore import load_data, load_shapes, load_graph, load_metadata
from rdaensemble import *


def main() -> None:
    args: argparse.Namespace = parse_args()

    data: Dict[str, Dict[str, int | str]] = load_data(args.data)
    # shapes: Dict[str, Any] = load_shapes(args.shapes)
    graph: Dict[str, List[str]] = load_graph(args.graph)
    metadata: Dict[str, Any] = load_metadata(args.state, args.data)
    N: int = int(metadata["D"])

    root_plan: List[Dict[str, str | int]] = read_csv(args.root, [str, int])
    initial_assignments: Dict[str, int | str] = {
        str(a["GEOID"]): a["DISTRICT"] for a in root_plan
    }

    # Pour the data & graph into a NetworkX graph for GerryChain

    nodes: List[Tuple] = [
        (
            i,
            {
                "GEOID": str(data[geoid]["GEOID"]),
                "TOTAL_POP": data[geoid]["TOTAL_POP"],
                "REP_VOTES": data[geoid]["REP_VOTES"],
                "DEM_VOTES": data[geoid]["DEM_VOTES"],
                "INITIAL": initial_assignments[geoid],
            },
        )
        for i, geoid in enumerate(data)
    ]
    node_index: Dict[str, int] = {geoid: i for i, geoid in enumerate(data)}
    back_map: Dict[int, str] = {v: k for k, v in node_index.items()}

    pairs: List[Tuple[str, str]] = mkAdjacencies(RDAGraph(graph))
    edges: List[Tuple[int, int]] = [
        (node_index[geoid1], node_index[geoid2]) for geoid1, geoid2 in pairs
    ]

    recom_graph = Graph()
    # recom_graph = nx.Graph()
    recom_graph.add_nodes_from(nodes)
    recom_graph.add_edges_from(edges)

    elections = [
        Election("composite", {"Democratic": "DEM_VOTES", "Republican": "REP_VOTES"}),
    ]

    #

    my_updaters: dict[str, Tally] = {
        "population": updaters.Tally("TOTAL_POP", alias="population")
    }
    election_updaters: dict[str, Election] = {
        election.name: election for election in elections
    }
    my_updaters.update(election_updaters)  # type: ignore

    initial_partition = GeographicPartition(
        recom_graph, assignment="INITIAL", updaters=my_updaters
    )

    ideal_population = sum(initial_partition["population"].values()) / len(
        initial_partition
    )

    proposal = partial(
        recom,
        pop_col="TOTAL_POP",
        pop_target=ideal_population,
        epsilon=args.roughlyequal / 2,
        node_repeats=2,  # TODO: What is this?
    )

    compactness_bound = constraints.UpperBound(
        lambda p: len(p["cut_edges"]), 2 * len(initial_partition["cut_edges"])
    )

    pop_constraint = constraints.within_percent_of_ideal_population(
        initial_partition, args.roughlyequal
    )

    chain = MarkovChain(
        proposal=proposal,
        constraints=[pop_constraint, compactness_bound],
        accept=accept.always_accept,
        initial_state=initial_partition,
        total_steps=args.size,
    )

    ## Running the chain

    ensemble: Dict[str, Any] = ensemble_metadata(
        xx="NC",
        ndistricts=N,
        size=args.size,
        method="ReCom",
    )
    plans: List[Dict[str, str | float | Dict[str, int | str]]] = list()

    # TODO - Add logging
    for step, partition in enumerate(chain):
        print(f"... {step} ...")
        assert partition is not None
        assignments: Assignment = partition.assignment

        plan_name: str = f"{step:04d}"
        plan: Dict[str, int | str] = {
            back_map[node]: part for node, part in assignments.items()
        }
        plans.append({"name": plan_name, "plan": plan})  # No weights.

        ensemble["plans"] = plans

        write_json(args.plans, ensemble)


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
    # parser.add_argument(
    #     "--shapes",
    #     type=str,
    #     help="Shapes abstract file",
    # )
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
        "--size", type=int, default=1000, help="Number of maps to generate"
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
        # "shapes": "../rdabase/data/NC/NC_2020_shapes_simplified.json",
        "graph": "../rdabase/data/NC/NC_2020_graph.json",
        "root": "../rdaroot/output/NC20C_RMfRST_100_rootmap.csv",
        "plans": "ensembles/NC20C_ReCom_1000_plans.json",
        "log": "ensembles/NC20C_ReCom_1000_log.txt",
        "size": 10,
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###


### END ###
