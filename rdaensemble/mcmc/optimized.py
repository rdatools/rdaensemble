"""
GENERATE AN ENSEMBLE OF MAPS using RECOM

NOTE - This is an exploration of ReCom's SingleMetricOptimizer feature.
NOTE - It is a clone of ensemble.py with the addition of the SingleMetricOptimizer feature.
       Shared code has been moved to helpers.py.

TODO - Rationalize this into one driver function w/ 3 helper functions.
"""

from typing import Any, List, Dict

import numpy as np

from gerrychain.partition.assignment import Assignment


def run_simulated_annealing_chain(
    optimizer,
    size: int,
    back_map: Dict[int, str],
    logfile,
    *,
    debug: bool = False,  # NOTE - Added size
) -> List[Dict[str, str | float | Dict[str, int | str]]]:
    """
    Run an optimized Markov chain.

    NOTE - The same as run_chain in ensemble.py, except using an optimizer chain and simulated annealing.
    """

    plans: List[Dict[str, str | float | Dict[str, int | str]]] = list()

    print()
    print("SIMULATED ANNEALING")
    print("===================")

    min_scores = np.zeros(size)
    for step, partition in enumerate(
        optimizer.simulated_annealing(
            size,
            optimizer.jumpcycle_beta_function(200, 800),
            beta_magnitude=1,
            with_progress_bar=False,
        )
    ):
        print(f"{step:04d}: Best score: {optimizer.best_score} ...")
        min_scores[step] = optimizer.best_score
        if not debug:
            print(f"... {step:04d} ...", file=logfile)
            assert partition is not None
            assignments: Assignment = partition.assignment

            # Convert the ReCom partition to a plan.
            plan: Dict[str, int | str] = {
                back_map[node]: part for node, part in assignments.items()
            }
            plan_name: str = f"{step:04d}"
            plans.append({"name": plan_name, "plan": plan})  # No weights.
        else:
            # print(f"      Min. scores: {min_scores}")
            pass

    # TODO - Do something with min_scores

    return plans


def run_short_bursts_chain(
    optimizer,
    size: int,
    back_map: Dict[int, str],
    logfile,
    *,
    debug: bool = False,  # NOTE - Added size
) -> List[Dict[str, str | float | Dict[str, int | str]]]:
    """
    Run an optimized Markov chain.

    NOTE - The same as run_chain in ensemble.py, except using an optimizer chain and short bursts.
    """

    plans: List[Dict[str, str | float | Dict[str, int | str]]] = list()

    print()
    print("SHORT BURSTS")
    print("============")

    min_scores = np.zeros(size)
    burst_length: int = 5
    for step, partition in enumerate(
        optimizer.short_bursts(
            burst_length, size // burst_length, with_progress_bar=False
        )
    ):
        print(f"{step:04d}: Best score: {optimizer.best_score} ...")
        min_scores[step] = optimizer.best_score
        if not debug:
            print(f"... {step:04d} ...", file=logfile)
            assert partition is not None
            assignments: Assignment = partition.assignment

            # Convert the ReCom partition to a plan.
            plan: Dict[str, int | str] = {
                back_map[node]: part for node, part in assignments.items()
            }
            plan_name: str = f"{step:04d}"
            plans.append({"name": plan_name, "plan": plan})  # No weights.
        else:
            # print(f"      Min. scores: {min_scores}")
            pass

    # TODO - Do something with min_scores

    return plans


def run_tilted_runs_chain(
    optimizer,
    size: int,
    back_map: Dict[int, str],
    logfile,
    *,
    debug: bool = False,  # NOTE - Added size
) -> List[Dict[str, str | float | Dict[str, int | str]]]:
    """
    Run an optimized Markov chain.

    NOTE - The same as run_chain in ensemble.py, except using an optimizer chain and tilted runs.
    """

    plans: List[Dict[str, str | float | Dict[str, int | str]]] = list()

    print()
    print("TILTED RUNS")
    print("===========")

    min_scores = np.zeros(size)
    for step, partition in enumerate(
        optimizer.tilted_run(size, p=0.125, with_progress_bar=False)
    ):
        print(f"{step:04d}: Best score: {optimizer.best_score} ...")
        min_scores[step] = optimizer.best_score
        if not debug:
            print(f"... {step:04d} ...", file=logfile)
            assert partition is not None
            assignments: Assignment = partition.assignment

            # Convert the ReCom partition to a plan.
            plan: Dict[str, int | str] = {
                back_map[node]: part for node, part in assignments.items()
            }
            plan_name: str = f"{step:04d}"
            plans.append({"name": plan_name, "plan": plan})  # No weights.
        else:
            # print(f"      Min. scores: {min_scores}")
            pass

    # TODO - Do something with min_scores

    return plans


### END ###
