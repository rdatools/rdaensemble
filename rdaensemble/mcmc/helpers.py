"""
HELPERS FOR GENERATING AN ENSEMBLE OF MAPS using RECOM
"""

from typing import Any, List, Dict, Tuple, Optional, Callable

from functools import partial
import json, shapely.geometry

from gerrychain import (
    GeographicPartition,
    Graph,
    MarkovChain,
    updaters,
    constraints,
    accept,
    Election,
)
from gerrychain.tree import bipartition_tree
from gerrychain.updaters import Tally
from gerrychain.constraints import contiguous
from gerrychain.optimization import SingleMetricOptimizer  # TODO - Add Gingleator

from rdabase import Graph as RDAGraph, mkAdjacencies, GeoID


def prep_data(
    initialplan: List[Dict[str, str | int]],
    data: Dict[str, Dict[str, int | str]],
    graph: Dict[str, List[str]],
    shapes: Optional[Dict[str, Any]] = None,
) -> Tuple[Graph, List[Election], Dict[int, str]]:
    """Prepare the data for ReCom."""

    initial_assignments: Dict[str, int | str] = {
        str(a["GEOID"]): a["DISTRICT"] for a in initialplan
    }

    nodes: List[Tuple] = []
    for i, geoid in enumerate(data):
        attrs: Dict[str, Any] = {
            "GEOID": str(data[geoid]["GEOID"]),
            "COUNTY": GeoID(geoid).county[2:],
            "TOTAL_POP": data[geoid]["TOTAL_POP"],
            "REP_VOTES": data[geoid]["REP_VOTES"],
            "DEM_VOTES": data[geoid]["DEM_VOTES"],
            "INITIAL": initial_assignments[geoid],
            # TODO - Need to update this to include VAP data
        }

        if shapes is not None:
            simplified_poly = shapes[geoid]
            shp = shapely.Polygon(simplified_poly["exterior"])
            geojson = shapely.geometry.mapping(shp)
            attrs["geometry"] = geojson

        node: Tuple = (i, attrs)

        nodes.append(node)

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
    size: int,
    metric: Optional[Callable],
    recom_graph: Graph,
    elections: List[Election],
    roughly_equal: float,
    elasticity: float,
    countyweight: float,
    node_repeats: int,
) -> Any:
    """Set up the Markov chain."""

    my_updaters: dict[str, Any] = {
        "population": updaters.Tally("TOTAL_POP", alias="population"),
        "perimeter": updaters.perimeter,
        "area": updaters.Tally("area", alias="area"),
    }  # TODO - Compactness
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

    chain: Any = None
    if metric is not None:
        chain = SingleMetricOptimizer(
            proposal=my_proposal,
            constraints=my_constraints,
            initial_state=initial_partition,
            optimization_metric=metric,
            maximize=False,
        )
    else:
        chain = MarkovChain(
            proposal=my_proposal,
            constraints=my_constraints,
            accept=accept.always_accept,
            initial_state=initial_partition,
            total_steps=size,
        )

    return chain


### END ###
