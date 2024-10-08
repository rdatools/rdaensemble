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

        demos_by_district: List[Dict[str, float]] = calc_demo_pcts_by_district(
            partition
        )
        results: dict[str, float] = calc_alt_minority_opportunity(
            statewide_demos, demos_by_district
        )
        oppty_pct: float = (
            results["opportunity_districts"] / results["proportional_opportunities"]
        )

        return oppty_pct

    return minority_proxy


def calc_demo_pcts_by_district(partition: Dict[str, Any]) -> List[Dict[str, float]]:
    """Calculate minority VAP %'s by district."""

    n_districts: int = len(partition)
    total_vap_field: str = census_fields[1]
    demos_by_district: List[Dict[str, float]] = [
        defaultdict(float) for _ in range(n_districts)
    ]

    for i in range(1, n_districts + 1):  # NOTE - Generalize for str districts
        j: int = i - 1
        for demo in census_fields[2:]:  # Skip total population & total VAP
            simple_demo: str = demo.split("_")[0].lower()
            demos_by_district[j][simple_demo] = (
                partition[demo][i] / partition[total_vap_field][i]
            )

    return demos_by_district


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


optimization_metrics: Dict[str, Any] = {
    "proportionality": proportionality_proxy,
    "competitiveness": competitiveness_proxy,
    "minority": minority_dummy,  # Replace this as necessary
    "compactness": compactness_proxy,
    "splitting": splitting_proxy,
}


### METRICS FOR PAIRS OF DIMENSIONS ###

starting_values: Dict[str, float] = {"x": -1.0, "y": -1.0}


def make_combined_metric(
    y_metric: Callable[..., float], x_metric: Callable[..., float]
) -> Callable[..., float]:
    """Combine two metrics into a single metric."""

    def optimization_metric(partition: Dict[str, Any]) -> float:
        """Combine the two metrics into a single metric."""

        global starting_values

        y_val: float = y_metric(partition)
        x_val: float = x_metric(partition)

        distance: float = (y_val**2 + x_val**2) ** 0.5

        if starting_values["x"] < 0.0 and starting_values["y"] < 0.0:
            starting_values["x"] = x_val
            starting_values["y"] = y_val
            # print(f"Starting y: {starting_values['y']}, x: {starting_values['x']}")
            return distance

        # Subtract a penalty from the starting point for not being NE of it
        if x_val < starting_values["x"] or y_val < starting_values["y"]:
            penalty: float = 0.10
            distance = (
                (starting_values["y"] ** 2 + starting_values["x"] ** 2) ** 0.5
            ) * (1 - penalty)

        # print(f"Current y: {y_val}, x: {x_val}, distance: {distance}")

        return distance

    return optimization_metric


### MISCELLANEOUS ###

optimize_methods: Dict[str, Callable] = {
    "simulated_annealing": simulated_annealing,
    "short_bursts": short_bursts,
    "tilted_runs": tilted_runs,
}

num_cut_edges: Callable = lambda p: len(p["cut_edges"])

### END ###
