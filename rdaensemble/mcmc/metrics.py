"""
TODO - PAIRWISE OPTIMIZATION

METRICS FOR OPTIMIZING TRADE-OFF FRONTIERS USING RECOM
"""

from typing import Any, List, Dict, Callable

import warnings

warnings.warn = lambda *args, **kwargs: None

from gerrychain.updaters import CountySplit

import rdapy as rda

from .optimized import (
    simulated_annealing,
    short_bursts,
    tilted_runs,
)


### METRICS FOR INDIVIDUAL DIMENSIONS ###


def proportionality_proxy(partition: Dict[str, Any]) -> float:
    """Use the EG of a partition as a proxy for disproportionality.

    Invert it so bigger is better.
    """

    eg: float = abs(partition["election_composite"].efficiency_gap())

    return 1 - eg


def competitiveness_proxy(partition: Dict[str, Any]) -> float:
    """Estimate the competitiveness of a partition as a percentage the # of districts."""

    Vf_array: List[float] = partition["election_composite"].percents("Democratic")

    cD: float = rda.est_competitive_districts(Vf_array)
    cDf: float = cD / len(partition)

    return cDf


def minority_dummy(partition):
    """A dummy function for minority representation."""

    assert False, "Minority optimization is built into Gingelator."


def minority_proxy(partition: Dict[str, Any]) -> float:
    """Estimate the opportunity for minority representation.

    "TOTAL_VAP": data[geoid]["TOTAL_VAP"],
    "MINORITY_VAP": data[geoid]["MINORITY_VAP"],
    "REP_VOTES": data[geoid]["REP_VOTES"],
    "DEM_VOTES": data[geoid]["DEM_VOTES"],

    """

    return 0.0  # TODO: Implement this function


def compactness_proxy(partition: Dict[str, Any]) -> float:
    """Estimate the compactness of a partition, using just the average Polsby-Popper (i.e., not also Reock)."""

    measurement: float = sum(partition["polsby-popper"].values()) / len(partition)

    return measurement


def splitting_proxy(partition: Dict[str, Any]) -> float:
    """Count the number of counties split by a partition. Return the percentage of counties split."""

    splits_by_county = partition["splits_by_county"]

    nsplits: int = 0
    for _, info in splits_by_county.items():
        if info.split != CountySplit.NOT_SPLIT:
            nsplits += 1

    n_counties: int = len(splits_by_county)
    split_pct: float = nsplits / n_counties

    return split_pct


### METRICS FOR PAIRS OF DIMENSIONS ###

# TODO
# metrics: Dict[str, Any] = {
#     "proportionality": {"metric": proportionality_proxy, "bigger_is_better": False},
#     "competitiveness": {"metric": competitiveness_proxy, "bigger_is_better": True},
#     "minority": {"metric": minority_dummy, "bigger_is_better": True},
#     "compactness": {"metric": compactness_proxy, "bigger_is_better": True},
#     "splitting": {"metric": splitting_proxy, "bigger_is_better": False},
# }
# metric: Callable = metrics[optimize_for]["metric"]
# bigger_is_better: bool = metrics[optimize_for]["bigger_is_better"]


### MISCELLANEOUS ###

optimize_methods: Dict[str, Callable] = {
    "simulated_annealing": simulated_annealing,
    "short_bursts": short_bursts,
    "tilted_runs": tilted_runs,
}

num_cut_edges: Callable = lambda p: len(p["cut_edges"])

### END ###
