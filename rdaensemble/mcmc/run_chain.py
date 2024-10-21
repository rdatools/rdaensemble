"""
GENERATE AN ENSEMBLE OF MAPS using RECOM
"""

from typing import Any, List, Dict, Set

import sys
from collections import defaultdict, Counter

from gerrychain.partition.assignment import Assignment

from rdabase import time_function


@time_function
def run_unbiased_chain(
    chain,
    back_map: Dict[int, str],
    logfile,
    *,
    keep: int = sys.maxsize,  # Keep all plans, by default
    random_start: bool = False,  # So district offsets can be adjusted
    burn_in: int = 0,
    sample: int = 0,
) -> List[Dict[str, str | float | Dict[str, int | str]]]:
    """Run a Markov chain."""

    assert burn_in == 0, "Don't burn-in."
    assert sample == 0, "Don't sample."

    plans: List[Dict[str, str | float | Dict[str, int | str]]] = list()
    district_offset: int = 1 if random_start else 0

    plans_kept: int = 0
    past_districts: Set = set()
    prev_districts: Set = set()
    reincarnateds = Counter()

    for step, partition in enumerate(chain):
        if burn_in > 0:
            if step < burn_in:
                print(f"Burning in   {step:06d}        ...")
                continue
            elif step == burn_in:
                print(f"Burn-in done {step-1:06d}        ...", file=logfile)

        print(f"Recombining  {step:06d}        ...")

        assert partition is not None
        assignments: Assignment = partition.assignment
        plan: Dict[str, int | str] = {
            back_map[node]: part + district_offset for node, part in assignments.items()
        }

        ############################ DEBUG ####################################

        # TODO - Maybe handle duplicate plan.

        geoids_by_district: List[Set[str]] = group_keys_by_value(plan)
        curr_districts: Set[int] = {hash_set(d) for d in geoids_by_district}

        not_in_prev: Set[int] = curr_districts - prev_districts
        reincarnatations: Set[int] = not_in_prev & past_districts

        if len(prev_districts - curr_districts) == 0 and prev_districts:
            print(f"Same plan 2x {step:06d}        <<<")
            print(f"Same plan 2x {step:06d}        <<<", file=logfile)
        elif len(prev_districts - curr_districts) != 2 and prev_districts:
            print(
                f"prev_districts: {prev_districts}, curr_districts: {curr_districts}, length: {len(prev_districts - curr_districts)}"
            )
        elif len(curr_districts - prev_districts) != 2 and prev_districts:
            print(
                f"prev_districts: {prev_districts}, curr_districts: {curr_districts}, length: {len(curr_districts - prev_districts)}"
            )

        if reincarnatations:
            for num in reincarnatations:
                reincarnateds[num] += 1
            print(f"Reincarnated {step:06d}        {reincarnateds}")
            print(f"Reincarnated {step:06d}        {reincarnateds}", file=logfile)

        past_districts.update(prev_districts)
        prev_districts = curr_districts

        #######################################################################

        plan_name: str = f"{plans_kept:04d}"
        plans_kept += 1
        plans.append({"name": plan_name, "plan": plan})  # No weights.

        print(f"Keeping plan {step:06d} ({plan_name}) ...")
        print(f"Keeping plan {step:06d} ({plan_name}) ...", file=logfile)

        if plans_kept >= keep:
            break

    print(f"Final reincarnated districts: {reincarnateds}")
    print(f"Final reincarnated districts: {reincarnateds}", file=logfile)

    return plans


def hash_set(s):
    return hash(frozenset(s))


def group_keys_by_value(dictionary):
    value_to_keys = defaultdict(set)
    for key, value in dictionary.items():
        value_to_keys[value].add(key)
    return list(value_to_keys.values())


### END ###
