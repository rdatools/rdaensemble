"""
TODO - PAIRWISE OPTIMIZATION

METRICS FOR OPTIMIZING TRADE-OFF FRONTIERS USING RECOM
"""

from typing import Any, List, Dict, Callable, Optional
from collections import defaultdict

import warnings

warnings.warn = lambda *args, **kwargs: None

from gerrychain.updaters import CountySplit

import rdapy as rda

from rdabase import census_fields

from .optimized import (
    simulated_annealing,
    short_bursts,
    tilted_runs,
)


### TODO - IMPORT THESE FROM RDASCORE ###


def calc_alt_minority_opportunity(
    statewide_demos: dict[str, float], demos_by_district: list[dict[str, float]]
) -> dict[str, float]:
    """Estimate ALTERNATE minority opportunity (everything except the table which is used in DRA)."""

    n_districts: int = len(demos_by_district)

    # Determine statewide proportional minority districts by single demographics (ignoring'White')
    districts_by_demo: dict[str, int] = {
        x: rda.calc_proportional_districts(statewide_demos[x], n_districts)
        for x in rda.DEMOGRAPHICS[1:]
    }

    # Sum the statewide proportional districts for each single demographic
    total_proportional: int = sum(
        [v for k, v in districts_by_demo.items() if k not in ["white", "minority"]]
    )

    # Sum the opportunities for minority represention in each district
    oppty_by_demo: dict[str, float] = defaultdict(float)
    for district in demos_by_district:
        for d in rda.DEMOGRAPHICS[1:]:  # Ignore 'white'
            # NOTE - Use the est_alt_minority_opportunity above, instead of est_minority_opportunity in rdapy.
            oppty_by_demo[d] += est_alt_minority_opportunity(district[d], d)

    # The # of opportunity districts for each separate demographic and all minorities
    od: float = sum(
        [v for k, v in oppty_by_demo.items() if k not in ["white", "minority"]]
    )
    cd: float = oppty_by_demo["minority"]

    # The # of proportional districts for each separate demographic and all minorities
    pod: float = total_proportional
    pcd: float = districts_by_demo["minority"]

    results: dict[str, float] = {
        # "pivot_by_demographic": table, # For this, use dra-analytics instead
        "opportunity_districts": od,
        "proportional_opportunities": pod,
        "coalition_districts": cd,
        "proportional_coalitions": pcd,
        # "details": {} # None
    }

    return results


def est_alt_minority_opportunity(mf: float, demo: Optional[str] = None) -> float:
    """Estimate the ALTERNATE opportunity for a minority representation.

    NOTE - Shift minority proportions up, so 37% minority scores like 52% share,
      but use the uncompressed seat probability distribution. This makes a 37%
      district have a ~70% chance of winning, and a 50% district have a >99% chance.
      Below 37 % has no chance.
    NOTE - Sam Wang suggest 90% probability for a 37% district. That seems a little
      too abrupt and all or nothing, so I backed off to the ~70%.
    """

    assert mf >= 0.0

    range: list[float] = [0.37, 0.50]

    shift: float = 0.15  # For Black VAP % (and Minority)
    dilution: float = 0.50  # For other demos, dilute the Black shift by half
    if demo and (demo not in ["black", "minority"]):
        shift *= dilution

    wip_num: float = mf + shift
    oppty: float = (
        # NOTE - This is the one-line change from est_minority_opportunity in rdapy,
        # i.e., don't clip VAP % below 37%.
        max(min(rda.est_seat_probability(wip_num), 1.0), 0.0)
        # 0.0 if (mf < range[0]) else min(rda.est_seat_probability(wip_num), 1.0)
    )

    return oppty


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
