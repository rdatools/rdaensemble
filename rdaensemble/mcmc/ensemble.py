"""
GENERATE AN ENSEMBLE OF MAPS using RECOM
"""

from typing import Any, List, Dict

from gerrychain.partition.assignment import Assignment

from rdabase import Graph as RDAGraph, mkAdjacencies, GeoID


def run_unbiased_chain(
    chain,
    size: int,
    back_map: Dict[int, str],
    logfile,
    *,
    debug: bool = False,
) -> List[Dict[str, str | float | Dict[str, int | str]]]:
    """Run a Markov chain."""

    plans: List[Dict[str, str | float | Dict[str, int | str]]] = list()

    for step, partition in enumerate(chain):
        print(f"... {step:04d} ...")
        print(f"... {step:04d} ...", file=logfile)
        assert partition is not None
        assignments: Assignment = partition.assignment

        # Convert the ReCom partition to a plan.
        plan: Dict[str, int | str] = {
            back_map[node]: part for node, part in assignments.items()
        }
        plan_name: str = f"{step:04d}"
        plans.append({"name": plan_name, "plan": plan})  # No weights.

    return plans


### END ###
