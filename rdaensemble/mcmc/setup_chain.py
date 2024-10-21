"""
SETUP AN UNBIASED RECOM CHAIN
"""

from typing import Any, List, Dict, Tuple, Callable, NamedTuple

from functools import partial

from gerrychain import (
    Partition,
    GeographicPartition,
    Graph,
    MarkovChain,
    updaters,
    constraints,
    accept,
    Election,
)
from gerrychain.tree import bipartition_tree, uniform_spanning_tree, recursive_tree_part
from gerrychain.constraints import contiguous
from gerrychain.proposals import recom


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

    def __repr__(self):
        def represent_value(field, value):
            if field == "accept":
                return f"<function {value.__name__} at {hex(id(value))}>"
            return repr(value)

        return f"{', '.join(f'{field}={represent_value(field, getattr(self, field))}' for field in self._fields)}"


def setup_unbiased_markov_chain(
    plan_type: str,
    n_districts: int,
    size: int,
    recom_graph: Graph,
    elections: List[Election],
    *,
    random_start: bool = False,
) -> Tuple[Any, ReComConfig]:
    """Set up an unbiased Markov chain."""

    """
    Parameters - TODO
    - How should roughly_equal values relate to the *resulting* population deviations that we want?
    - Should countyweight weight change, based on the type of plan? the number of districts?
    """
    config: ReComConfig = ReComConfig(
        roughly_equal=(0.01 if plan_type == "congress" else 0.10),
        elasticity=2.0,
        countyweight=0.75,
        accept=accept.always_accept,
        node_repeats=1,
        max_attempts=100,
        allow_pair_reselection=True,
        default_sampling=True,
    )

    # Updaters
    my_updaters: dict[str, Any] = {
        "cut_edges": updaters.cut_edges,
        "population": updaters.Tally("TOTAL_POP", alias="population"),
    }
    election_updaters: dict[str, Election] = {
        election.name: election for election in elections
    }
    my_updaters.update(election_updaters)  # type: ignore

    # Initial partition
    initial_partition: Partition | GeographicPartition
    if random_start:
        assert (
            plan_type == "congress"
        ), "Random start not implemented for state legislative plans."
        bpt = partial(bipartition_tree, max_attempts=99999)
        # bpt = partial(
        #     bipartition_tree, spanning_tree_fn=uniform_spanning_tree, max_attempts=99999
        # )
        rtp = partial(recursive_tree_part, method=bpt)
        initial_partition = GeographicPartition.from_random_assignment(
            graph=recom_graph,
            n_parts=n_districts,
            epsilon=config.roughly_equal,  # / 2,  # 1/2 of what you want to end up with
            pop_col="TOTAL_POP",
            updaters=my_updaters,
            method=rtp,
        )
    else:
        initial_partition = GeographicPartition(
            recom_graph, assignment="INITIAL", updaters=my_updaters
        )

    # Ideal population
    ideal_population = sum(initial_partition["population"].values()) / len(
        initial_partition
    )

    # Weights
    my_weights = {"COUNTY": config.countyweight}

    # Bipartition tree method
    bpt = bipartition_tree
    if not config.default_sampling:
        bpt = partial(bipartition_tree, spanning_tree_fn=uniform_spanning_tree)
    method = partial(
        bpt,
        max_attempts=config.max_attempts,
        allow_pair_reselection=config.allow_pair_reselection,
    )

    # Proposal
    my_proposal: Callable = partial(
        recom,
        pop_col="TOTAL_POP",
        pop_target=ideal_population,
        epsilon=config.roughly_equal / 2,  # 1/2 of what you want to end up with
        region_surcharge=my_weights,
        node_repeats=config.node_repeats,
        method=method,
    )

    # Constraints
    pop_constraint = constraints.within_percent_of_ideal_population(
        initial_partition, config.roughly_equal
    )
    # Per Moon Duchin, not strictly necessary.
    # compactness_bound = constraints.UpperBound(
    #     lambda p: len(p["cut_edges"]),
    #     config.elasticity * len(initial_partition["cut_edges"]),
    # )
    my_constraints: List = [
        contiguous,
        pop_constraint,
    ]
    # if bound_compactness:
    #     my_constraints.append(compactness_bound)

    # Chain
    chain: Any = MarkovChain(
        proposal=my_proposal,
        constraints=my_constraints,
        accept=config.accept,
        initial_state=initial_partition,
        total_steps=size,
    )

    return chain, config


### END ###
