"""
GENERATE AN OPTIMIZED ENSEMBLE OF PLANS using RECOM and its SingleMetricOptimizer feature.

TODO - Remove dead code.
"""

from typing import Any, List, Dict, Optional, Callable

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
from gerrychain.optimization import SingleMetricOptimizer  # TODO - Add Gingleator
from gerrychain.metrics.compactness import polsby_popper

from gerrychain.partition.assignment import Assignment


def setup_optimized_markov_chain(
    proposal: Callable,
    recom_graph: Graph,
    elections: List[Election],
    roughly_equal: float,
    # elasticity: float,
    # countyweight: float,
    node_repeats: int,
    *,
    ndistricts: int,
    metric: Callable,
    maximize: bool = True,
) -> Any:
    """Set up the Markov chain."""

    my_updaters: dict[str, Any] = {
        "cut_edges": updaters.cut_edges,
        "population": updaters.Tally("TOTAL_POP", alias="population"),
        "polsby-popper": polsby_popper,
    }
    election_updaters: dict[str, Election] = {
        election.name: election for election in elections
    }
    my_updaters.update(election_updaters)  # type: ignore

    initial_partition = GeographicPartition.from_random_assignment(
        graph=recom_graph,
        n_parts=ndistricts,
        epsilon=roughly_equal / 2,  # 1/2 of what you want to end up with
        pop_col="TOTAL_POP",
        updaters=my_updaters,
    )
    # initial_partition = GeographicPartition(
    #     recom_graph, assignment="INITIAL", updaters=my_updaters
    # )

    ideal_population = sum(initial_partition["population"].values()) / len(
        initial_partition
    )

    my_proposal: Callable
    my_constraints: List
    # my_weights = {"COUNTY": countyweight}

    method = partial(bipartition_tree, max_attempts=100, allow_pair_reselection=True)

    my_proposal = partial(
        proposal,
        pop_col="TOTAL_POP",
        pop_target=ideal_population,
        epsilon=roughly_equal / 2,  # 1/2 of what you want to end up with
        # region_surcharge=my_weights,  # was: weight_dict=my_weights in 0.3.0
        node_repeats=node_repeats,
        method=method,
    )

    # compactness_bound = constraints.UpperBound(
    #     lambda p: len(p["cut_edges"]),
    #     elasticity * len(initial_partition["cut_edges"]),
    # )  # Per Moon Duchin, not strictly necessary.

    pop_constraint = constraints.within_percent_of_ideal_population(
        initial_partition, roughly_equal
    )
    my_constraints = [contiguous, pop_constraint]

    chain: Any = SingleMetricOptimizer(
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
    # size: int,
    back_map: Dict[int, str],
    logfile,
    *,
    label: str = "Simulated Annealing",
    method: Callable = simulated_annealing,
    max_steps: int = 1000,
    stop_after: int = 10,  # TODO
) -> List[Dict[str, str | float | Dict[str, int | str]]]:
    """Run an optimized Markov chain -- Accumulate the plans along the path from a random starting point to the best plan found."""

    plans: List[Dict[str, str | float | Dict[str, int | str]]] = list()

    print()
    print(f"{label.upper()}")
    print("===================")

    best_score: float = 0.0
    for step, partition in enumerate(method(optimizer, max_steps)):
        print(f"... {step:04d} ...")
        if optimizer.best_score > best_score:
            best_score = optimizer.best_score

            print(f"... Improves metric to {best_score} ...")
            print(f"... {step:04d} ...", file=logfile)
            print(f"... Improves metric to {best_score} ...", file=logfile)
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
