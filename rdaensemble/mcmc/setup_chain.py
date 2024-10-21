"""
SETUP AN UNBIASED RECOM CHAIN
"""

from typing import Any, List, Dict, Tuple, Callable, NamedTuple

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
from gerrychain.tree import bipartition_tree, uniform_spanning_tree
from gerrychain.constraints import contiguous
from gerrychain.proposals import recom
from gerrychain.partition.assignment import Assignment  # TODO


class ReComConfig(NamedTuple):
    """Configuration for ReCom."""

    roughly_equal: float
    elasticity: float
    countyweight: float
    accept: Callable[..., bool]
    node_repeats: int
    max_attempts: int
    allow_pair_reselection: bool
    default_sampling: bool


def setup_unbiased_markov_chain_REVISED(
    # proposal: Callable,
    plan_type: str,
    n_districts: int,
    size: int,
    recom_graph: Graph,
    elections: List[Election],
    *,
    random_start: bool = False,
) -> Tuple[Any, Dict[str, Any]]:
    """Set up an unbiased Markov chain."""

    config: ReComConfig = ReComConfig(
        roughly_equal=0.01 if plan_type == "congress" else 0.10,
        elasticity=2.0,
        countyweight=0.75,
        accept=accept.always_accept,
        node_repeats=1,
        max_attempts=100,
        allow_pair_reselection=True,
        default_sampling=True,
    )
    settings: Dict[str, Any] = config._asdict()

    foo: Tuple[Callable[..., bool]] = (accept.always_accept,)

    my_updaters: dict[str, Any] = {
        "cut_edges": updaters.cut_edges,
        "population": updaters.Tally("TOTAL_POP", alias="population"),
    }
    election_updaters: dict[str, Election] = {
        election.name: election for election in elections
    }
    my_updaters.update(election_updaters)  # type: ignore

    # TODO - Can we get rid of the random_start option?
    initial_partition = (
        GeographicPartition.from_random_assignment(
            graph=recom_graph,
            n_parts=n_districts,
            epsilon=0.01,  # TODO - Should this depend on plan_type a la 'roughly_equal?!?
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

    my_weights = {"COUNTY": config.countyweight}

    bpt = bipartition_tree
    if not config.default_sampling:
        bpt = partial(bipartition_tree, spanning_tree_fn=uniform_spanning_tree)
    method = partial(
        bpt,
        max_attempts=config.max_attempts,
        allow_pair_reselection=config.allow_pair_reselection,
    )

    my_proposal: Callable = partial(
        recom,
        pop_col="TOTAL_POP",
        pop_target=ideal_population,
        epsilon=config.roughly_equal / 2,  # 1/2 of what you want to end up with
        region_surcharge=my_weights,
        node_repeats=config.node_repeats,
        method=method,
    )

    # Per Moon Duchin, not strictly necessary.
    # compactness_bound = constraints.UpperBound(
    #     lambda p: len(p["cut_edges"]),
    #     config.elasticity * len(initial_partition["cut_edges"]),
    # )

    pop_constraint = constraints.within_percent_of_ideal_population(
        initial_partition, config.roughly_equal
    )
    my_constraints: List = [
        contiguous,
        pop_constraint,
    ]  # was [contiguous, compactness_bound, pop_constraint]
    # if bound_compactness:
    #     my_constraints.append(compactness_bound)

    chain: Any = MarkovChain(
        proposal=my_proposal,
        constraints=my_constraints,
        accept=config.accept,
        initial_state=initial_partition,
        total_steps=size,
    )

    return chain, settings


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
    bound_compactness: bool = True,
    wilson_sampling: bool = False,
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

    # Select the bipartition tree method
    bpt = bipartition_tree
    if wilson_sampling:
        bpt = partial(bipartition_tree, spanning_tree_fn=uniform_spanning_tree)
    method = partial(bpt, max_attempts=100, allow_pair_reselection=True)
    # was: method = partial(bipartition_tree, max_attempts=100, allow_pair_reselection=True)

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
    my_constraints: List = [
        contiguous,
        pop_constraint,
    ]  # was [contiguous, compactness_bound, pop_constraint]
    if bound_compactness:
        my_constraints.append(compactness_bound)

    chain: Any = MarkovChain(
        proposal=my_proposal,
        constraints=my_constraints,
        accept=accept.always_accept,
        initial_state=initial_partition,
        total_steps=size,
    )

    return chain


### END ###
