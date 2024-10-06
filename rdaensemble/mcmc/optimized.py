"""
GENERATE AN OPTIMIZED ENSEMBLE OF PLANS using RECOM and its SingleMetricOptimizer feature.
"""

from typing import Any, List, Dict, Optional, Callable

import sys
from functools import partial

from gerrychain import (
    GeographicPartition,
    Graph,
    updaters,
    constraints,
    Election,
)
from gerrychain.tree import bipartition_tree
from gerrychain.constraints import contiguous
from gerrychain.optimization import SingleMetricOptimizer, Gingleator
from gerrychain.metrics.compactness import polsby_popper

from gerrychain.partition.assignment import Assignment


def setup_optimized_markov_chain(
    proposal: Callable,
    recom_graph: Graph,
    elections: List[Election],
    roughly_equal: float,
    node_repeats: int,
    *,
    dimension: str,
    metric: Callable,
    maximize: bool,
) -> Any:
    """Set up the Markov chain."""

    my_updaters: dict[str, Any] = {
        "cut_edges": updaters.cut_edges,
        "population": updaters.Tally("TOTAL_POP", alias="population"),
        "polsby-popper": polsby_popper,
        "splits_by_county": updaters.county_splits("splits_by_county", "COUNTY"),
        "TOTAL_VAP": updaters.Tally("TOTAL_VAP"),
        "WHITE_VAP": updaters.Tally("WHITE_VAP"),
        "HISPANIC_VAP": updaters.Tally("HISPANIC_VAP"),
        "BLACK_VAP": updaters.Tally("BLACK_VAP"),
        "NATIVE_VAP": updaters.Tally("NATIVE_VAP"),
        "ASIAN_VAP": updaters.Tally("ASIAN_VAP"),
        "PACIFIC_VAP": updaters.Tally("PACIFIC_VAP"),
        "MINORITY_VAP": updaters.Tally("MINORITY_VAP"),
    }
    election_updaters: dict[str, Election] = {
        election.name: election for election in elections
    }
    my_updaters.update(election_updaters)  # type: ignore

    initial_partition = GeographicPartition(
        recom_graph, assignment="INITIAL", updaters=my_updaters
    )

    ideal_population = sum(initial_partition["population"].values()) / len(
        initial_partition
    )

    my_proposal: Callable
    my_constraints: List

    method = partial(bipartition_tree, max_attempts=100, allow_pair_reselection=True)

    my_proposal = partial(
        proposal,
        pop_col="TOTAL_POP",
        pop_target=ideal_population,
        epsilon=roughly_equal / 2,  # 1/2 of what you want to end up with
        node_repeats=node_repeats,
        method=method,
    )

    pop_constraint = constraints.within_percent_of_ideal_population(
        initial_partition, roughly_equal
    )
    my_constraints = [contiguous, pop_constraint]

    chain: Any
    if dimension == "minority":
        chain = Gingleator(
            proposal=my_proposal,
            constraints=my_constraints,
            initial_state=initial_partition,
            minority_pop_col="MINORITY_VAP",
            total_pop_col="TOTAL_VAP",
            score_function=Gingleator.reward_partial_dist,
        )
    else:
        chain = SingleMetricOptimizer(
            proposal=my_proposal,
            constraints=my_constraints,
            initial_state=initial_partition,
            optimization_metric=metric,
            maximize=maximize,
        )

    return chain


def simulated_annealing(
    optimizer, total_steps: int, *, duration_hot: int = 200, duration_cold: int = 800
) -> Any:
    """Simulated annealing"""

    partitions = optimizer.simulated_annealing(
        total_steps,
        optimizer.jumpcycle_beta_function(duration_hot, duration_cold),
        beta_magnitude=1,
        with_progress_bar=True,
    )

    return partitions


def short_bursts(optimizer, total_steps: int, *, burst_length: int = 5) -> Any:
    """Short bursts"""

    partitions = optimizer.short_bursts(
        burst_length, total_steps // burst_length, with_progress_bar=True
    )

    return partitions


def tilted_runs(optimizer, total_steps: int, *, p: float = 0.125) -> Any:
    """Tilted runs"""

    partitions = optimizer.tilted_run(total_steps, p=p, with_progress_bar=True)

    return partitions


def run_optimized_chain(
    optimizer,
    steps: int,
    back_map: Dict[int, str],
    prefix: str,
    *,
    bigger_is_better: bool,
    method: Callable = short_bursts,
) -> List[Dict[str, str | float | Dict[str, int | str]]]:
    """Run an optimized Markov chain -- Accumulate the plans along the path from the starting point to the best plan found."""

    plans: List[Dict[str, str | float | Dict[str, int | str]]] = list()

    best_score: float = sys.float_info.min if bigger_is_better else sys.float_info.max
    for step, partition in enumerate(method(optimizer, steps)):
        if (bigger_is_better and optimizer.best_score > best_score) or (
            not bigger_is_better and optimizer.best_score < best_score
        ):
            best_score = optimizer.best_score

            print(f"=> Metric improved to {best_score}.")

            assert partition is not None
            assignments: Assignment = partition.assignment

            # Convert the ReCom partition to a plan.
            plan: Dict[str, int | str] = {
                back_map[node]: part for node, part in assignments.items()
            }
            plan_name: str = f"{prefix}-{step:04d}"
            plans.append({"name": plan_name, "plan": plan})  # No weights.

    return plans


### END ###
