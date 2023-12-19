"""
ID NOTABLE MAPS IN AN ENSEMBLE
"""

from typing import Any, Dict, List

metrics: List[str] = [
    "proportionality",
    "competitiveness",
    "minority",
    "compactness",
    "splitting",
]
dimensions: List[int] = list(range(5))


def id_notable_maps(scores: List[Dict[str, Any]], filters: List[int]) -> Dict[str, Any]:
    """Find the notable maps in a scored ensemble of maps."""

    output: Dict[str, Any] = dict()
    notable_maps: List[Dict[str, Any]] = [{m: "None", "ratings": []} for m in metrics]

    total: int = 0
    qualifying: int = 0

    for s in scores:
        total += 1
        ratings: List[int] = [int(s[m]) for m in metrics]
        if not qualifying_map(ratings, filters):
            continue

        for d in dimensions:
            if better_map(ratings, notable_maps[d], d):
                notable_maps[d][metrics[d]] = s["map"]
                notable_maps[d]["ratings"] = ratings

        qualifying += 1

    output["size"] = total
    output["filters"] = filters
    output["qualifying"] = qualifying
    output["notable_maps"] = notable_maps

    return output


def qualifying_map(ratings: List[int], filters: List[int]) -> bool:
    return all([ratings[i] >= filters[i] for i in dimensions])


def better_map(
    ratings: List[int], current_best: Dict[str, Any], dimension: int
) -> bool:
    if current_best[metrics[dimension]] == "None":
        return True
    if (ratings[dimension] > current_best["ratings"][dimension]) or (
        ratings[dimension] == current_best["ratings"][dimension]
        and sum(ratings) > sum(current_best["ratings"])
    ):
        return True
    else:
        return False


### END ###
