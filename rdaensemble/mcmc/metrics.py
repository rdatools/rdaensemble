"""
METRICS FOR OPTIMIZING TRADE-OFF FRONTIERS USING RECOM
"""

from typing import Any, List, Dict, Callable, Optional
from collections import defaultdict

import warnings

warnings.warn = lambda *args, **kwargs: None

from gerrychain.updaters import CountySplit

import rdapy as rda

from rdabase import census_fields
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

    return normalize_proportionality_proxy(eg)


def normalize_proportionality_proxy(eg: float) -> float:
    """Normalize the EG measurement to be between 0 and 1, bigger is better.

    NOTE - This could also narrow the range to give a broader spread, e.g., TODO.
    """

    return 1 - eg


def competitiveness_proxy(partition: Dict[str, Any]) -> float:
    """Estimate the competitiveness of a partition as a percentage the # of districts."""

    Vf_array: List[float] = partition["election_composite"].percents("Democratic")

    cD: float = rda.est_competitive_districts(Vf_array)
    cDf: float = cD / len(partition)

    return normalize_competitiveness_proxy(cDf)


def normalize_competitiveness_proxy(cDf: float) -> float:
    """Normalize the competitiveness measurement to be between 0 and 1, bigger is better.

    NOTE - Right now, this is a no-op. This could narrow the range though, e.g., [0.0 - 0.75].
    """

    return cDf


def minority_dummy(partition):
    """A dummy function for minority representation."""

    assert False, "Minority optimization is built into Gingelator."


def make_minority_proxy(statewide_demos: Dict[str, float]) -> Callable[..., float]:

    def minority_proxy(partition: Dict[str, Any]) -> float:
        """Estimate the opportunity for minority representation."""

        n_districts: int = len(partition)
        demos_by_district: List[Dict[str, float]] = [
            defaultdict(float) for _ in range(n_districts + 1)
        ]

        for i in range(1, n_districts + 1):  # NOTE - Generalize for str districts
            for demo in census_fields[2:]:  # Skip total population & total VAP
                demos_by_district[i][demo] = partition[demo][i]

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

    return normalize_compactness_proxy(measurement)


def normalize_compactness_proxy(measurement: float) -> float:
    """Normalize the compactness measurement to be between 0 and 1, bigger is better.

    NOTE - Right now, this is a no-op. This could narrow the range though, e.g., TODO.
    """

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

    return normalize_splitting_proxy(split_pct)


def normalize_splitting_proxy(pct: float) -> float:
    """Normalize the percentage of counties split to be between 0 and 1, bigger is better.

    NOTE - This could narrow the range to give a broader spread, e.g., TODO.
    """

    return 1 - pct


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
