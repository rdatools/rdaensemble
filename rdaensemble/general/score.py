"""
SCORE AN ENSEMBLE OF PLANS
"""

from typing import List, Dict, Set, Any

import sys

from rdabase import (
    mkPoints,
    Point,
    index_points,
    IndexedPoint,
    populations,
    index_geoids,
    index_assignments,
    Assignment,
    IndexedWeightedAssignment,
    calc_energy,
)
from rdascore import analyze_plan
from .compactness import cuts_and_boundaries
from .utils import make_plan


def score_ensemble(
    plans: List[Dict[str, str | float | Dict[str, int | str]]],
    data: Dict[str, Dict[str, int | str]],
    shapes: Dict[str, Any],
    graph: Dict[str, List[str]],
    metadata: Dict[str, Any],
    alt_minority: bool = False,
    epsilon: float = 0.01,
) -> List[Dict]:
    """Score an ensemble of maps."""

    points: List[Point] = mkPoints(data, shapes)

    indexed_geoids: Dict[str, int] = index_geoids(points)
    indexed_points: List[IndexedPoint] = index_points(points)

    ipop_by_geoid: Dict[str, int] = populations(data)
    fpop_by_geoid: Dict[str, float] = {
        k: float(max(epsilon, v)) for k, v in ipop_by_geoid.items()
    }

    scores: List[Dict] = list()

    for i, p in enumerate(plans):
        plan_name: str = str(p["name"])
        print(f"Scoring {i}: {plan_name} ...")

        try:
            plan_dict: Dict[str, int | str] = p["plan"]  # type: ignore
            assignments: List[Assignment] = make_plan(plan_dict)
            indexed_assignments: List[IndexedWeightedAssignment] = index_assignments(
                assignments, indexed_geoids, fpop_by_geoid
            )

            # Make sure districts are indexed [1, 2, 3, ...]
            district_ids: Set[int | str] = set()
            for a in assignments:
                district_ids.add(a.district)
            if min(district_ids) != 1:
                print("Districts must be indexed [1, 2, 3, ...]")
                sys.exit(1)

            energy: float = calc_energy(indexed_assignments, indexed_points)

            record: Dict[str, Any] = dict()
            record["map"] = plan_name
            record["energy"] = energy

            cut_pct, boundary_pct = cuts_and_boundaries(plan_dict, graph)
            record["cut_edges"] = cut_pct
            record["boundary_nodes"] = boundary_pct

            scorecard: Dict[str, Any] = analyze_plan(
                assignments,
                data,
                shapes,
                graph,
                metadata,
                alt_minority=alt_minority,
            )

            if alt_minority:
                scorecard["minority"] = scorecard["minority_alt"]
                scorecard.pop("minority_alt")

            record.update(scorecard)
            scores.append(record)
            pass  # for break point

        except Exception as e:
            print(f"Failure: {e}")
            pass

    return scores


def is_defined_opportunity_district(
    dem_votes: int,
    rep_votes: int,
    group_dem_votes: int,
    group_rep_votes: int,
    white_dem_votes: int,
    white_rep_votes: int,
) -> bool:
    """Is a district a defined minority opportunity district?

    Parameters:
    dem_votes: int - Democratic votes in the district
    rep_votes: int - Republican votes in the district
    group_dem_votes: int - Democratic votes in the minority group (e.g., Black or Hispanic) in the district
    group_rep_votes: int - Republican votes in the minority group in the district
    white_dem_votes: int - Democratic votes in the white + other group in the district
    white_rep_votes: int - Republican votes in the white + other group in the district

    Returns:
    bool - True if the district is defined as a minority opportunity district, False otherwise

    """

    # The minority-preferred candidate is one who received a majority of the minority group's votes
    minority_preferred_candidate_is_dem: bool = group_dem_votes > group_rep_votes

    # Two conditions must be met for a district to be a defined minority opportunity district:
    # 1 - The minority preferred candidate must win the district
    minority_preferred_candidate_won: bool = (
        minority_preferred_candidate_is_dem and dem_votes > rep_votes
    ) or (not minority_preferred_candidate_is_dem and rep_votes > dem_votes)

    # 2 - The minority group votes for the preferred candidate must outnumber the white+other votes for the preferred candidate
    minority_votes_outnumber_white_votes: bool = (
        minority_preferred_candidate_is_dem and group_dem_votes > white_dem_votes
    ) or (not minority_preferred_candidate_is_dem and group_rep_votes > white_rep_votes)

    return minority_preferred_candidate_won and minority_votes_outnumber_white_votes


def count_defined_opportunity_districts() -> int:
    """Count the number of defined Black & Hispanic opportunity districts in a plan."""

    return 42


### END ###
