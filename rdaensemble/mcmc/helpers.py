"""
HELPERS FOR GENERATING AN ENSEMBLE OF MAPS using RECOM

TODO - Delete dead code.
"""

from typing import Any, List, Dict, Tuple, Callable

from functools import partial

from gerrychain import (
    GeographicPartition,
    Graph,
    # MarkovChain,
    updaters,
    constraints,
    # accept,
    Election,
)
from gerrychain.tree import bipartition_tree
from gerrychain.updaters import Tally
from gerrychain.constraints import contiguous
from gerrychain.optimization import SingleMetricOptimizer  # , Gingleator

# from tqdm import tqdm

from rdabase import Graph as RDAGraph, mkAdjacencies, GeoID


def prep_data(
    initialplan: List[Dict[str, str | int]],
    data: Dict[str, Dict[str, int | str]],
    graph: Dict[str, List[str]],
) -> Tuple[Graph, List[Election], Dict[int, str]]:
    """
    Prepare the data for ReCom.

    # NOTE - Unchanged from ensemble.py
    """

    initial_assignments: Dict[str, int | str] = {
        str(a["GEOID"]): a["DISTRICT"] for a in initialplan
    }

    nodes: List[Tuple] = [
        (
            i,
            {
                "GEOID": str(data[geoid]["GEOID"]),
                "COUNTY": GeoID(geoid).county[2:],
                "TOTAL_POP": data[geoid]["TOTAL_POP"],
                "REP_VOTES": data[geoid]["REP_VOTES"],
                "DEM_VOTES": data[geoid]["DEM_VOTES"],
                "INITIAL": initial_assignments[geoid],
                # TODO - Need to update this to include VAP data
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

    elections: List[Election] = [
        Election("composite", {"Democratic": "DEM_VOTES", "Republican": "REP_VOTES"}),
    ]

    return recom_graph, elections, back_map


def setup_markov_chain(
    proposal: Callable,
    # size: int, # NOTE - Removed this
    recom_graph: Graph,
    elections: List[Election],
    roughly_equal: float,
    elasticity: float,
    countyweight: float,
    node_repeats: int,
) -> Any:
    """
    Set up the Markov chain.

    NOTE - Tweaked to setup an optimizer chain using SingleMetricOptimizer.
    """

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

    my_proposal: Callable
    my_constraints: List
    my_weights = {"COUNTY": countyweight}

    method = partial(bipartition_tree, allow_pair_reselection=True)

    my_proposal = partial(
        proposal,
        pop_col="TOTAL_POP",
        pop_target=ideal_population,
        epsilon=roughly_equal / 2,  # 1/2 of what you want to end up with
        region_surcharge=my_weights,  # was: weight_dict=my_weights in 0.3.0
        node_repeats=node_repeats,
        method=method,
    )

    compactness_bound = constraints.UpperBound(
        lambda p: len(p["cut_edges"]),
        elasticity * len(initial_partition["cut_edges"]),
    )  # Per Moon Duchin, not strictly necessary.

    pop_constraint = constraints.within_percent_of_ideal_population(
        initial_partition, roughly_equal
    )
    my_constraints = [contiguous, compactness_bound, pop_constraint]

    # NOTE - Added an objective function for SingleMetricOptimizer
    # TODO - Figure out proxies for each of the 5 ratings dimensions
    num_cut_edges = lambda p: len(p["cut_edges"])

    # NOTE - Modified this
    # chain = MarkovChain(
    optimizer = SingleMetricOptimizer(
        proposal=my_proposal,
        constraints=my_constraints,
        # accept=accept.always_accept, # NOTE - Removed this
        initial_state=initial_partition,
        # total_steps=size, # NOTE - Removed this
        optimization_metric=num_cut_edges,  # NOTE - Added this
        maximize=False,  # NOTE - Added this
    )

    return optimizer


### END ###
