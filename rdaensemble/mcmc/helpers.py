"""
HELPERS FOR GENERATING AN ENSEMBLE OF MAPS using RECOM
"""

from typing import Any, List, Dict, Tuple, Optional

import shapely.geometry

from gerrychain import (
    Graph,
    Election,
)

from rdabase import Graph as RDAGraph, mkAdjacencies, GeoID


def prep_data(
    data: Dict[str, Dict[str, int | str]],
    graph: Dict[str, List[str]],
    shapes: Optional[Dict[str, Any]] = None,
    *,
    initial_plan: List[Dict[str, str | int]] = [],
) -> Tuple[Graph, List[Election], Dict[int, str]]:
    """Prepare the data for ReCom."""

    initial_assignments: Dict[str, int | str] = {}
    if initial_plan:
        assert "GEOID" in initial_plan[0] or "GEOID20" in initial_plan[0]
        assert "DISTRICT" in initial_plan[0] or "District" in initial_plan[0]
        geoid_field: str = "GEOID20" if "GEOID20" in initial_plan[0] else "GEOID"
        district_field: str = (
            "District" if "District" in initial_plan[0] else "DISTRICT"
        )

        initial_assignments: Dict[str, int | str] = {
            str(a[geoid_field]): a[district_field] for a in initial_plan
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
            "TOTAL_VAP": data[geoid]["TOTAL_VAP"],
            "WHITE_VAP": data[geoid]["WHITE_VAP"],
            "HISPANIC_VAP": data[geoid]["HISPANIC_VAP"],
            "BLACK_VAP": data[geoid]["BLACK_VAP"],
            "NATIVE_VAP": data[geoid]["NATIVE_VAP"],
            "ASIAN_VAP": data[geoid]["ASIAN_VAP"],
            "PACIFIC_VAP": data[geoid]["PACIFIC_VAP"],
            "MINORITY_VAP": data[geoid]["MINORITY_VAP"],
            # "MINORITY_VAP": int(data[geoid]["BLACK_VAP"])
            # + int(data[geoid]["HISPANIC_VAP"]),  # Not sure why I used this proxy originally ...
            "REP_VOTES": data[geoid]["REP_VOTES"],
            "DEM_VOTES": data[geoid]["DEM_VOTES"],
            # "INITIAL": initial_assignments[geoid],
        }
        if initial_assignments:
            attrs["INITIAL"] = initial_assignments[geoid]

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
        Election(
            "election_composite", {"Democratic": "DEM_VOTES", "Republican": "REP_VOTES"}
        ),
    ]

    return recom_graph, elections, back_map


### END ###
