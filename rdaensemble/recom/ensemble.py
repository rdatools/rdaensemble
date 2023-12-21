"""
GENERATE AN ENSEMBLE OF MAPS using RECOM
"""

from typing import List, Dict, Tuple

from functools import partial

from gerrychain import (
    GeographicPartition,
    Graph,
    MarkovChain,
    updaters,
    constraints,
    accept,
    Election,
)
from gerrychain.updaters import Tally
from gerrychain.proposals import recom
from gerrychain.partition.assignment import Assignment

from rdabase import Graph as RDAGraph, mkAdjacencies


def gen_recom_ensemble(
    size: int,  # Number of random maps to generate
    steps: int,  # Number of steps to run each Markov chain <<< TODO
    initial: List[Dict[str, str | int]],  # Initial district assignments
    seed: int,  # Starting random seed <<< TODO
    data: Dict[str, Dict[str, int | str]],
    graph: Dict[str, List[str]],
    logfile,
    *,
    roughly_equal: float = 0.02,
    elasticity: float = 2.0,
    node_repeats: int = 1,
) -> List[Dict[str, str | float | Dict[str, int | str]]]:
    """Generate an ensemble of maps using ReCom."""

    # Prep the data

    initial_assignments: Dict[str, int | str] = {
        str(a["GEOID"]): a["DISTRICT"] for a in initial
    }

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
    recom_graph.add_nodes_from(nodes)
    recom_graph.add_edges_from(edges)

    elections = [
        Election("composite", {"Democratic": "DEM_VOTES", "Republican": "REP_VOTES"}),
    ]

    # Set up the Markov chain

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
        epsilon=roughly_equal / 2,  # 1/2 of what you want to end up with
        node_repeats=node_repeats,
    )

    compactness_bound = constraints.UpperBound(
        lambda p: len(p["cut_edges"]),
        elasticity * len(initial_partition["cut_edges"]),
    )

    pop_constraint = constraints.within_percent_of_ideal_population(
        initial_partition, roughly_equal
    )

    chain = MarkovChain(
        proposal=proposal,
        constraints=[pop_constraint, compactness_bound],
        accept=accept.always_accept,
        initial_state=initial_partition,
        total_steps=size,
    )

    # Run ReCom

    plans: List[Dict[str, str | float | Dict[str, int | str]]] = list()

    for step, partition in enumerate(chain):
        print(f"... {step} ...")
        print(f"... {step} ...", file=logfile)
        assert partition is not None
        assignments: Assignment = partition.assignment

        plan_name: str = f"{step:04d}"
        plan: Dict[str, int | str] = {
            back_map[node]: part for node, part in assignments.items()
        }
        plans.append({"name": plan_name, "plan": plan})  # No weights.

    return plans


### END ###
