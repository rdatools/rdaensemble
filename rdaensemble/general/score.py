"""
SCORE AN ENSEMBLE OF PLANS
"""

from typing import List, Dict, Set, NamedTuple, Any

import sys
from collections import defaultdict, OrderedDict


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
    read_csv,
    time_function,
)
from rdascore import analyze_plan
from .minority import (
    InferredVotes,
    aggregate_votes_by_district,
    count_defined_opportunity_districts,
)
from .utils import make_plan


@time_function
def score_ensemble(
    plans: List[Dict[str, str | float | Dict[str, int | str]]],
    data: Dict[str, Dict[str, int | str]],
    shapes: Dict[str, Any],
    graph: Dict[str, List[str]],
    metadata: Dict[str, Any],
    *,
    est_votes: Dict[str, InferredVotes] = dict(),
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

    N: int = int(metadata["D"])

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

            record: OrderedDict[str, Any] = OrderedDict()
            record["map"] = plan_name

            scorecard: Dict[str, Any] = analyze_plan(
                assignments,
                data,
                shapes,
                graph,
                metadata,
            )

            # Remove by-district compactness & splitting from from the scores
            by_district: List[Dict[str, float]] = scorecard.pop("by_district")

            # Add the (flat) scores
            record.update(scorecard)

            # Add 'energy' as 'population_compactness' as the last compactness score
            record = insert_pair_after(
                record,
                "spanning_tree_score",
                "population_compactness",
                energy,
            )

            # Count defined minority opportunity districts (MOD)
            if est_votes:
                aggregated_votes: Dict[int | str, InferredVotes] = (
                    aggregate_votes_by_district(assignments, est_votes, N)
                )
                votes_by_district: List[InferredVotes] = list(
                    aggregated_votes.values()
                )[1:]

                oppty_district_count: int
                mods: List[int | str]
                oppty_district_count, mods = count_defined_opportunity_districts(
                    votes_by_district
                )

                mod_scores: Dict[str, float | int] = defaultdict(float)
                mod_scores["mod_districts"] = int(
                    oppty_district_count
                )  # TODO - Type is wrong
                for d in mods:
                    i: int = int(d) - 1
                    mod_scores["mod_reock"] += by_district[i]["reock"]
                    mod_scores["mod_polsby_popper"] += by_district[i]["polsby"]
                    mod_scores["mod_spanning_tree_score"] += by_district[i][
                        "spanning_tree_score"
                    ]
                    mod_scores["mod_district_splitting"] += by_district[i][
                        "district_splitting"
                    ]
                mod_scores = {
                    k: v / oppty_district_count
                    for k, v in mod_scores.items()
                    if k != "defined_opportunity_districts"
                }

                record = insert_dict_after(
                    record,
                    "alt_coalition_districts",
                    mod_scores,
                )
                pass

            scores.append(record)
            pass

        except Exception as e:
            print(f"Failure: {e}")
            pass

    return scores


def insert_pair_after(d, key, new_key, new_value):
    if key not in d:
        raise KeyError(f"Key '{key}' not found in the OrderedDict")

    items = list(d.items())
    insert_position = items.index((key, d[key])) + 1
    items.insert(insert_position, (new_key, new_value))

    return OrderedDict(items)


def insert_dict_after(original_dict: OrderedDict, key, new_dict):
    return OrderedDict(
        k_v
        for k_v in (
            (k, v)
            for items in (
                list(original_dict.items())[
                    : list(original_dict.keys()).index(key) + 1
                ],
                list(
                    new_dict.items()
                    if isinstance(new_dict, OrderedDict)
                    else OrderedDict(new_dict).items()
                ),
                list(original_dict.items())[
                    list(original_dict.keys()).index(key) + 1 :
                ],
            )
            for k, v in items
        )
    )


### END ###
