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
from gerrychain.constraints import contiguous

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

    assert len(data) == len(graph) - 1  # -1 for OUT_OF_STATE
    if shapes:
        assert len(data) == len(shapes)

    nodes: List[Tuple] = []
    for i, geoid in enumerate(data):
        attrs: Dict[str, Any] = {
            "GEOID": str(data[geoid]["GEOID"]),
            "COUNTY": GeoID(geoid).county[2:],
            "TOTAL_POP": data[geoid]["TOTAL_POP"],
            "REP_VOTES": data[geoid]["REP_VOTES"],
            "DEM_VOTES": data[geoid]["DEM_VOTES"],
            "INITIAL": initial_assignments[geoid],
            # TODO - Add VAP data for minority opportunity
        }

        if shapes:  # is not None:
            simplified_poly = shapes[geoid]

            shp = shapely.Polygon(simplified_poly["exterior"])
            geojson = shapely.geometry.mapping(shp)
            attrs["geometry"] = geojson

            attrs["area"] = simplified_poly["area"]

            if "OUT_OF_STATE" in simplified_poly["arcs"]:
                attrs["boundary_node"] = True
                attrs["boundary_perim"] = simplified_poly["arcs"]["OUT_OF_STATE"]
            else:
                attrs["boundary_node"] = False

        node: Tuple = (i, attrs)

        nodes.append(node)

    node_index: Dict[str, int] = {geoid: i for i, geoid in enumerate(data)}
    back_map: Dict[int, str] = {v: k for k, v in node_index.items()}

    pairs: List[Tuple[str, str]] = mkAdjacencies(RDAGraph(graph))
    # Unique pairs of geoids where geoid1 < geoid2 & OUT_OF_STATE removed

    edges: List[Tuple] = []
    shared_perims: Dict[Tuple[int, int], float] = {}
    for geoid1, geoid2 in pairs:
        n1: int = node_index[geoid1]
        n2: int = node_index[geoid2]
        edge: Tuple = (n1, n2) if n1 < n2 else (n2, n1)

        if shapes:  # is not None:
            simplified_poly = shapes[geoid1]
            shared_perims[edge] = simplified_poly["arcs"][geoid2]

        edges.append(edge)

    if shapes:  # is not None:
        assert len(edges) == len(shared_perims)

    recom_graph = Graph()
    recom_graph.add_nodes_from(nodes)
    if shapes:  # is not None:
        for edge in edges:
            recom_graph.add_edge(edge[0], edge[1], shared_perim=shared_perims[edge])
            # recom_graph.add_edges_from([edge], shared_perim=shared_perims[edge])
    else:
        recom_graph.add_edges_from(edges)

    elections: List[Election] = [
        Election("composite", {"Democratic": "DEM_VOTES", "Republican": "REP_VOTES"}),
    ]

    return recom_graph, elections, back_map


### END ###
