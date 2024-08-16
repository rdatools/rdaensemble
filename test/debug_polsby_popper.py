#!/usr/bin/env python3

"""
SANDBOX - THROWAWAY CODE

$ ./sandbox.py

"""

from typing import Any, List, Dict, Tuple

import random
import warnings
from collections import defaultdict

warnings.warn = lambda *args, **kwargs: None

from gerrychain.proposals import recom

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


def main() -> None:

    data: Dict[str, Dict[str, int | str]] = load_data(
        "../rdabase/data/NC/NC_2020_data.csv"
    )
    shapes: Dict[str, Any] = load_shapes(
        "../rdabase/data/NC/NC_2020_shapes_simplified.json"
    )
    graph: Dict[str, List[str]] = load_graph("../rdabase/data/NC/NC_2020_graph.json")
    metadata: Dict[str, Any] = load_metadata(
        "NC", "../rdabase/data/NC/NC_2020_data.csv"
    )

    plan_rows = read_csv("../tradeoffs/root_maps/NC20C_root_map.csv", [str, int])

    N: int = int(metadata["D"])
    seed: int = starting_seed("NC", N)

    #

    plan: dict[str, int | str] = {row["GEOID"]: row["DISTRICT"] for row in plan_rows}

    inverted_plan: defaultdict[int | str, set[str]] = defaultdict(set)
    for k, v in plan.items():
        inverted_plan[v].add(k)

    #

    random.seed(seed)

    recom_graph, elections, back_map = prep_data(plan_rows, data, graph, shapes)
    node_index: Dict[str, int] = {v: k for k, v in back_map.items()}

    ## Compare the arc/edge lengths in the recom_graph to the original graph ##

    input_total_area: float = 0.0
    input_exterior_perims: Dict[Tuple[str, str], float] = {}
    input_interior_perims: Dict[Tuple[str, str], float] = {}

    for from_geoid, abstract in shapes.items():
        input_total_area += abstract["area"]

        for to_geoid, shared_border in abstract["arcs"].items():
            pair: Tuple[str, str] = (
                (from_geoid, to_geoid)
                if from_geoid < to_geoid
                else (to_geoid, from_geoid)
            )

            if "OUT_OF_STATE" in pair:
                if pair not in input_exterior_perims:
                    input_exterior_perims[pair] = shared_border
            else:
                if pair not in input_interior_perims:
                    input_interior_perims[pair] = shared_border

    input_shapes: int = len(shapes)
    input_exterior_perim: float = sum(input_exterior_perims.values())
    input_exterior_arcs: int = len(input_exterior_perims)
    input_interior_perim: float = sum(input_interior_perims.values())
    input_interior_arcs: int = len(input_interior_perims)
    input_total_perim: float = input_exterior_perim + input_interior_perim

    pass

    recom_nodes: int = len(recom_graph.nodes)
    recom_total_area: float = 0.0
    recom_exterior_perim: float = 0.0
    recom_exterior_arcs: int = 0
    recom_interior_perim: float = 0.0
    recom_interior_arcs: int = len(recom_graph.edges)
    recom_total_perim: float = 0.0

    for node, node_attr in recom_graph.nodes.items():
        recom_total_area += node_attr["area"]

        if node_attr["boundary_node"]:
            recom_exterior_perim += node_attr["boundary_perim"]
            recom_exterior_arcs += 1

    mismatched_arcs: int = 0
    for edge, edge_attr in recom_graph.edges.items():
        recom_interior_perim += edge_attr["shared_perim"]

        geoid: str = back_map[edge[0]]
        neighbor_geoid: str = back_map[edge[1]]
        input_interior_arc: float = shapes[geoid]["arcs"][neighbor_geoid]
        recom_interior_arc: float = edge_attr["shared_perim"]

        if recom_interior_arc != input_interior_arc:
            mismatched_arcs += 1
            # print(
            #     f"Warning: input and recom interior arc lengths differ for {geoid} and {neighbor_geoid}!"
            # )

    recom_total_perim = recom_exterior_perim + recom_interior_perim

    print()
    print("These should match!")
    print(
        f"Input -- area ({input_shapes}): {input_total_area:.6f}, perimeter: {input_total_perim:.6f}, interior ({input_interior_arcs}): {input_interior_perim:.6f}, exterior ({input_exterior_arcs}): {input_exterior_perim:.6f}"
    )
    print(
        f"recom -- area ({recom_nodes}): {recom_total_area:.6f}, perimeter: {recom_total_perim:.6f}, interior ({recom_interior_arcs}): {recom_interior_perim:.6f}, exterior ({recom_exterior_arcs}): {recom_exterior_perim:.6f}"
    )
    print(f"Mismatched arcs: {mismatched_arcs}")

    pass

    ## End comparing arc/edge lengths ##

    for district, geoids in inverted_plan.items():
        total_area: float = 0.0
        exterior_perim: float = 0.0
        interior_perim: float = 0.0

        for geoid in geoids:
            node: int = node_index[geoid]
            node_attr = recom_graph.nodes[node]

            total_area += node_attr["area"]

            if node_attr["boundary_node"]:
                print(
                    f"District: {district}, exterior: {geoid}, length: {node_attr['boundary_perim']}"
                )
                exterior_perim += node_attr["boundary_perim"]

            for neighbor_geoid in graph[geoid]:
                if neighbor_geoid == "OUT_OF_STATE":
                    continue

                neighbor: int = node_index[neighbor_geoid]

                if plan[geoid] != plan[neighbor_geoid]:
                    edge: Tuple = (
                        (node, neighbor) if node < neighbor else (neighbor, node)
                    )
                    edge_attr = recom_graph.edges[edge]

                    print(
                        f"District: {district}, interior: {geoid}, length: {edge_attr['shared_perim']}"
                    )
                    interior_perim += edge_attr["shared_perim"]

                total_perim: float = exterior_perim + interior_perim

        print(
            f"District: {district}, {len(geoids)} geoids, area: {total_area:.6f}, perim: {total_perim:.6f} (exterior: {exterior_perim:.6f}, interior: {interior_perim:.6f})"
        )
        pass

    pass


if __name__ == "__main__":
    main()

pass  # Breakpoint

### END ###
