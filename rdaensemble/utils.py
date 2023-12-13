"""
MISCELLANEOUS UTILITIES
"""

from typing import Any, Dict, List


def plan_from_ensemble(
    plan_name: str, ensemble: Dict[str, Any]
) -> Dict[str, str | float | Dict[str, int | str]]:
    """Return the named plan from an ensemble."""

    plans: List[Dict[str, str | float | Dict[str, int | str]]] = ensemble["plans"]
    for p in plans:
        if p["name"] == plan_name:
            return p
    raise ValueError(f"Plan {plan_name} not found in ensemble")


### END ###
