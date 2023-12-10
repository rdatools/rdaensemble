"""
SCORE AN ENSEMBLE OF PLANS
"""

from typing import List, Dict, Tuple, Any

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


def score_ensemble(
    plans: List[Dict[str, str | float | Dict[str, int | str]]],
    data: Dict[str, Dict[str, int | str]],
    shapes: Dict[str, Any],
    graph: Dict[str, List[str]],
    metadata: Dict[str, Any],
) -> List[Dict]:
    """Score an ensemble of maps."""

    points: List[Point] = mkPoints(data, shapes)

    indexed_geoids: Dict[str, int] = index_geoids(points)
    indexed_points: List[IndexedPoint] = index_points(points)

    pop_by_geoid: Dict[str, int] = populations(data)

    scores: List[Dict] = list()

    for i, p in enumerate(plans):
        print(f"... {i} ...")

        try:
            # Get a plan
            plan_name: str = str(p["name"])
            plan_dict: Dict[str, int | str] = p["plan"]  # type: ignore
            assignments: List[Assignment] = make_plan(plan_dict)
            indexed_assignments: List[IndexedWeightedAssignment] = index_assignments(
                assignments, indexed_geoids, pop_by_geoid
            )

            # Calculate the energy
            energy: float = calc_energy(indexed_assignments, indexed_points)

            record: Dict[str, Any] = dict()
            record["map"] = plan_name
            record["energy"] = energy

            scorecard: Dict[str, Any] = analyze_plan(
                assignments,
                data,
                shapes,
                graph,
                metadata,
            )
            record.update(scorecard)
            scores.append(record)

        except Exception as e:
            print(f"Failure: {e}")
            pass

    return scores


def make_plan(assignments: Dict[str, int | str]) -> List[Assignment]:
    """Convert a dict of geoid: district assignments to a list of Assignments."""

    plan: List[Assignment] = [
        Assignment(geoid, district) for geoid, district in assignments.items()
    ]
    return plan


### END ###
