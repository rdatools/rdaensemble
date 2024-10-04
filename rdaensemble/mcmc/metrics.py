"""
METRICS FOR OPTIMIZING TRADE-OFF FRONTIERS USING RECOM
"""

from typing import Any, List, Dict, Optional, Callable

import warnings

warnings.warn = lambda *args, **kwargs: None

from gerrychain.updaters import CountySplit

import rdapy as rda


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
    """Count the number of counties split by a partition. Return the percentage of counties that are split."""

    counties = partition["split_counties"]

    nsplits: int = 0
    for _, info in counties.items():
        if info.split != CountySplit.NOT_SPLIT:
            nsplits += 1
    split_pct: float = nsplits / len(counties)

    return split_pct


### END ###
