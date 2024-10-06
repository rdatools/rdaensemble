"""
METRICS FOR OPTIMIZING TRADE-OFF FRONTIERS USING RECOM
"""

from typing import Any, List, Dict, Callable, Optional
from collections import defaultdict

import warnings

warnings.warn = lambda *args, **kwargs: None

from gerrychain.updaters import CountySplit

import rdapy as rda

from rdascore import calc_alt_minority_opportunity

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


def make_minority_proxy(statewide_demos: Dict[str, float]) -> Callable[..., float]:

    def minority_proxy(partition: Dict[str, Any]) -> float:
        """Estimate the opportunity for minority representation."""

        # total_vap: Dict[int, int] = partition["TOTAL_VAP"]
        white_vap: Dict[int, int] = partition["WHITE_VAP"]
        minority_vap: Dict[int, int] = partition["MINORITY_VAP"]
        black_vap: Dict[int, int] = partition["BLACK_VAP"]
        hispanic_vap: Dict[int, int] = partition["HISPANIC_VAP"]
        native_vap: Dict[int, int] = partition["NATIVE_VAP"]
        asian_vap: Dict[int, int] = partition["ASIAN_VAP"]
        pacific_vap: Dict[int, int] = partition["PACIFIC_VAP"]

        n_districts: int = len(partition)

        demos_by_district: List[Dict[str, float]] = [
            defaultdict(float) for _ in range(n_districts + 1)
        ]

        for i in range(1, n_districts + 1):  # NOTE - Generalize for str districts
            # demos_by_district[i]["TOTAL_VAP"] = total_vap[i]
            demos_by_district[i]["WHITE_VAP"] = white_vap[i]
            demos_by_district[i]["MINORITY_VAP"] = minority_vap[i]
            demos_by_district[i]["BLACK_VAP"] = black_vap[i]
            demos_by_district[i]["HISPANIC_VAP"] = hispanic_vap[i]
            demos_by_district[i]["NATIVE_VAP"] = native_vap[i]
            demos_by_district[i]["ASIAN_VAP"] = asian_vap[i]
            demos_by_district[i]["PACIFIC_VAP"] = pacific_vap[i]

        results: dict[str, float] = calc_alt_minority_opportunity(
            statewide_demos, demos_by_district
        )
        oppty_pct: float = (
            results["opportunity_districts"] / results["proportional_opportunities"]
        )

        return oppty_pct

    return minority_proxy


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

optimization_metrics: Dict[str, Any] = {
    "proportionality": proportionality_proxy,
    "competitiveness": competitiveness_proxy,
    "minority": minority_dummy,  # Replace this as necessary
    "compactness": compactness_proxy,
    "splitting": splitting_proxy,
}


### MISCELLANEOUS ###

optimize_methods: Dict[str, Callable] = {
    "simulated_annealing": simulated_annealing,
    "short_bursts": short_bursts,
    "tilted_runs": tilted_runs,
}

num_cut_edges: Callable = lambda p: len(p["cut_edges"])

### END ###
