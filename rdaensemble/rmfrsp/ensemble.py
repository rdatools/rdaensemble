"""
GENERATE AN ENSEMBLE OF RANDOM MAPS from RANDOM STARTING POINTS (RMfRSP)
"""

from typing import Dict, List, Tuple


def gen_rmfrsp_ensemble(
    size: int,  # Number of random maps to generate
    seed: int,  # Starting random seed
    data: Dict[str, Dict[str, int | str]],
    graph: Dict[str, List[str]],
    N: int,  # Number of districts
    logfile,
    *,
    roughly_equal: float = 0.02,
) -> List[Dict[str, str | float | Dict[str, int | str]]]:
    """Generate an ensemble of random maps from random starting points."""

    start: int = seed
    plans: List[Dict[str, str | float | Dict[str, int | str]]] = list()

    # TODO

    return plans


### END ###
