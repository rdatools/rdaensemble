#!/usr/bin/env python3

"""
GENERATE A ReCom ENSEMBLE 

To run:

$ scripts/recom_ensemble.py

TODO

"""

from typing import Any, List, Dict

from gerrychain import (
    GeographicPartition,
    Partition,
    Graph,
    MarkovChain,
    proposals,
    updaters,
    constraints,
    accept,
    Election,
)
from gerrychain.updaters import Tally, cut_edges
from gerrychain.proposals import recom
from functools import partial

from gerrychain.partition.assignment import Assignment

# import pandas

from rdabase import write_json
from rdaensemble import ensemble_metadata


def main() -> None:
    ## Setting up the initial districting plan

    graph = Graph.from_json("temp/PA_VTDs.json")

    pass  # TODO

    elections = [
        Election("SEN10", {"Democratic": "SEN10D", "Republican": "SEN10R"}),
        Election("SEN12", {"Democratic": "USS12D", "Republican": "USS12R"}),
        Election("SEN16", {"Democratic": "T16SEND", "Republican": "T16SENR"}),
        Election("PRES12", {"Democratic": "PRES12D", "Republican": "PRES12R"}),
        Election("PRES16", {"Democratic": "T16PRESD", "Republican": "T16PRESR"}),
    ]

    # Population updater, for computing how close to equality the district
    # populations are. "TOTPOP" is the population column from our shapefile.
    my_updaters: dict[str, Tally] = {
        "population": updaters.Tally("TOTPOP", alias="population")
    }

    # Election updaters, for computing election results using the vote totals
    # from our shapefile.
    election_updaters: dict[str, Election] = {
        election.name: election for election in elections
    }
    my_updaters.update(election_updaters)  # type: ignore

    initial_partition = GeographicPartition(
        graph, assignment="CD_2011", updaters=my_updaters
    )

    ## NOTE - Added

    back_map: Dict[int, str] = {
        i: graph._node[i]["GEOID10"] for i, n in enumerate(graph.nodes)
    }

    ## Proposal

    # The ReCom proposal needs to know the ideal population for the districts so that
    # we can improve speed by bailing early on unbalanced partitions.

    ideal_population = sum(initial_partition["population"].values()) / len(
        initial_partition
    )

    # We use functools.partial to bind the extra parameters (pop_col, pop_target, epsilon, node_repeats)
    # of the recom proposal.
    proposal = partial(
        recom,
        pop_col="TOTPOP",
        pop_target=ideal_population,
        epsilon=0.02,
        node_repeats=2,
    )

    ## Constraints

    compactness_bound = constraints.UpperBound(
        lambda p: len(p["cut_edges"]), 2 * len(initial_partition["cut_edges"])
    )

    pop_constraint = constraints.within_percent_of_ideal_population(
        initial_partition, 0.02
    )

    ## Configuring the Markov chain

    chain = MarkovChain(
        proposal=proposal,
        constraints=[pop_constraint, compactness_bound],
        accept=accept.always_accept,
        initial_state=initial_partition,
        total_steps=1000,
    )

    ## Running the chain

    ensemble: Dict[str, Any] = ensemble_metadata(
        xx="PA",
        ndistricts=18,
        size=1000,
        method="ReCom",
    )
    plans: List[Dict[str, str | float | Dict[str, int | str]]] = []

    for step, partition in enumerate(chain):
        print(f"... {step} ...")
        assert partition is not None
        assignments: Assignment = partition.assignment

        plan_name: str = f"{step:04d}"
        plan: Dict[str, int | str] = {
            back_map[node]: part for node, part in assignments.items()
        }
        plans.append({"name": plan_name, "plan": plan})  # No weights.

        ensemble["plans"] = plans

        write_json("ensembles/PAyyC_ReCom_1000_plans.json", ensemble)

    pass


if __name__ == "__main__":
    main()

### END ###
