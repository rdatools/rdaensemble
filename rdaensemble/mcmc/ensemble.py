"""
GENERATE AN ENSEMBLE OF MAPS using RECOM
"""

from typing import Any, List, Dict, Callable

from functools import partial

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
) -> List[Dict[str, str | float | Dict[str, int | str]]]:
    """Run a Markov chain."""

    plans: List[Dict[str, str | float | Dict[str, int | str]]] = list()
    district_offset: int = 1 if random_start else 0

    for step, partition in enumerate(chain):
        print(f"Recombining {step:04d} ...")
        print(f"Recombining {step:04d} ...", file=logfile)
        assert partition is not None
        assignments: Assignment = partition.assignment

        # Convert the ReCom partition to a plan.
        plan: Dict[str, int | str] = {
            back_map[node]: part + district_offset for node, part in assignments.items()
        }
        plan_name: str = f"{step:04d}"
        plans.append({"name": plan_name, "plan": plan})  # No weights.

    return plans


### END ###
