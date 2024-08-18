"""
GENERATE AN OPTIMIZED ENSEMBLE OF PLANS using RECOM and its SingleMetricOptimizer feature.
"""

from typing import Any, List, Dict, Callable

import numpy as np

from gerrychain.partition.assignment import Assignment

### OPTIMIZATION METHODS ###


def simulated_annealing(
    optimizer, size: int, *, duration_hot: int = 200, duration_cold: int = 800
) -> Any:
    """Simulated annealing"""

    partitions = optimizer.simulated_annealing(
        size,
        optimizer.jumpcycle_beta_function(duration_hot, duration_cold),
        beta_magnitude=1,
        with_progress_bar=False,
    )

    return partitions


def short_bursts(optimizer, size: int, *, burst_length: int = 5) -> Any:
    """Short bursts"""

    partitions = optimizer.short_bursts(
        burst_length, size // burst_length, with_progress_bar=False
    )

    return partitions


def tilted_runs(optimizer, size: int, *, p: float = 0.125) -> Any:
    """Tilted runs"""

    partitions = optimizer.tilted_run(size, p=p, with_progress_bar=False)

    return partitions


### RUN A RECOM CHAIN ###


def run_optimized_chain(
    optimizer,
    size: int,
    back_map: Dict[int, str],
    logfile,
    *,
    label: str = "Simulated Annealing",
    method: Callable = simulated_annealing,
    debug: bool = False,
) -> List[Dict[str, str | float | Dict[str, int | str]]]:
    """Run an optimized Markov chain."""

    plans: List[Dict[str, str | float | Dict[str, int | str]]] = list()

    print()
    print(f"{label.upper()}")
    print("===================")

    best_score: float = 0.0
    for step, partition in enumerate(method(optimizer, size)):
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
