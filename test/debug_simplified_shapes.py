#!/usr/bin/env python3

"""
DEBUG SIMPLIFIED SHAPES
"""

from typing import Any, List, Dict, Tuple

import random
import warnings
from collections import defaultdict

warnings.warn = lambda *args, **kwargs: None

from rdabase import (
    starting_seed,
    read_csv,
    load_data,
    load_shapes,
    load_graph,
    load_metadata,
    approx_equal,
)


def arcs_are_symmetric(shapes: Dict[str, Any]) -> bool:
    symmetric: bool = True
    narcs: int = 0
    nasymmetric: int = 0

    for from_geoid, abstract in shapes.items():
        for to_geoid, from_border in abstract["arcs"].items():
            if to_geoid != "OUT_OF_STATE":
                narcs += 1
                to_border = shapes[to_geoid]["arcs"][from_geoid]
                if not approx_equal(from_border, to_border, places=4):
                    symmetric = False
                    nasymmetric += 1
                    print(
                        f"Arcs between {from_geoid} & {to_geoid} are not symmetric: {from_border} & {to_border}."
                    )

    if not symmetric:
        print(f"Total arcs: {narcs}, non-symmetric arcs: {nasymmetric}")

    return symmetric


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

    ## Verify that arc lengths in simplified json are symmetric ##

    if arcs_are_symmetric(shapes):
        print("All arc lengths in simplified json are symmetric.")

    pass


if __name__ == "__main__":
    main()

pass  # Breakpoint

### END ###
