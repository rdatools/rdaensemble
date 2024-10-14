"""
GENERATE AN ENSEMBLE OF MAPS using RECOM
"""

from typing import Any, List, Dict, Set, Callable

from functools import partial
from collections import defaultdict

from gerrychain import (
    GeographicPartition,
    Graph,
    MarkovChain,
    updaters,
    constraints,
    accept,
    Election,
)
from gerrychain.tree import bipartition_tree
from gerrychain.constraints import contiguous

from gerrychain.partition.assignment import Assignment


def setup_unbiased_markov_chain(
    proposal: Callable,
    size: int,
    recom_graph: Graph,
    elections: List[Election],
    roughly_equal: float,
    elasticity: float,
    countyweight: float,
    node_repeats: int,
    *,
    n_districts: int,
    random_start: bool = False,
) -> Any:
    """Set up an unbiased (not optimized) Markov chain."""

    my_updaters: dict[str, Any] = {
        "cut_edges": updaters.cut_edges,
        "population": updaters.Tally("TOTAL_POP", alias="population"),
    }
    election_updaters: dict[str, Election] = {
        election.name: election for election in elections
    }
    my_updaters.update(election_updaters)  # type: ignore

    initial_partition = (
        GeographicPartition.from_random_assignment(
            graph=recom_graph,
            n_parts=n_districts,
            epsilon=0.01,
            pop_col="TOTAL_POP",
            updaters=my_updaters,
        )
        if random_start
        else GeographicPartition(
            recom_graph, assignment="INITIAL", updaters=my_updaters
        )
    )

    ideal_population = sum(initial_partition["population"].values()) / len(
        initial_partition
    )

    my_proposal: Callable
    my_weights = {"COUNTY": countyweight}

    method = partial(bipartition_tree, max_attempts=100, allow_pair_reselection=True)

    my_proposal = partial(
        proposal,
        pop_col="TOTAL_POP",
        pop_target=ideal_population,
        epsilon=roughly_equal / 2,  # 1/2 of what you want to end up with
        region_surcharge=my_weights,  # was: weight_dict=my_weights in 0.3.0
        node_repeats=node_repeats,
        method=method,
    )

    compactness_bound = constraints.UpperBound(
        lambda p: len(p["cut_edges"]),
        elasticity * len(initial_partition["cut_edges"]),
    )  # Per Moon Duchin, not strictly necessary.

    pop_constraint = constraints.within_percent_of_ideal_population(
        initial_partition, roughly_equal
    )
    my_constraints: List = [contiguous, compactness_bound, pop_constraint]

    chain: Any = MarkovChain(
        proposal=my_proposal,
        constraints=my_constraints,
        accept=accept.always_accept,
        initial_state=initial_partition,
        total_steps=size,
    )

    return chain


def run_unbiased_chain(
    chain,
    back_map: Dict[int, str],
    logfile,
    *,
    random_start: bool = False,
    burn_in: int = 1000,
    keep_total: int = 10000,
) -> List[Dict[str, str | float | Dict[str, int | str]]]:
    """Run a Markov chain."""

    plans: List[Dict[str, str | float | Dict[str, int | str]]] = list()
    district_offset: int = 1 if random_start else 0

    districts_seen: Set = set()
    plans_kept: int = 0

    for step, partition in enumerate(chain):
        if step < burn_in:
            print(f"Burning in {step:06d} ...")
            continue

        print(f"Considering {step:06d} ...")

        assert partition is not None
        assignments: Assignment = partition.assignment

        plan: Dict[str, int | str] = {
            back_map[node]: part + district_offset for node, part in assignments.items()
        }

        geoids_by_district: List[Set[str]] = group_keys_by_value(plan)
        district_hashes: List[int] = list()
        all_districts_new: bool = True

        for combo in geoids_by_district:
            district_hash: int = hash_set(combo)
            district_hashes.append(district_hash)
            if district_hash in districts_seen:
                all_districts_new = False
                break
        if not all_districts_new:
            continue  # Skip plans that have any districts that have already been seen.

        # This plan is unique.

        for district_hash in district_hashes:
            districts_seen.add(district_hash)

        plan_name: str = f"{plans_kept - 1:04d}"
        plans.append({"name": plan_name, "plan": plan})  # No weights.
        plans_kept += 1

        print(f"Keeping {plan_name} ({step:06d}) ...")
        print(f"Keeping {plan_name} ({step:06d}) ...", file=logfile)

        if plans_kept >= keep_total:
            break

    return plans


def hash_set(s):
    return hash(frozenset(s))


def group_keys_by_value(dictionary):
    value_to_keys = defaultdict(set)
    for key, value in dictionary.items():
        value_to_keys[value].add(key)
    return list(value_to_keys.values())


### END ###
