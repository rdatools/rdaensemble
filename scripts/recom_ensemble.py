#!/usr/bin/env python3

"""
GENERATE A ReCom ENSEMBLE (RECOM)

For example:

$ scripts/recom_ensemble.py \
  ...

For documentation, type:

$ scripts/recom_ensemble.py -h

"""

from gerrychain import Graph, Partition, Election, MarkovChain
from gerrychain.updaters import Tally, cut_edges
from gerrychain.constraints import single_flip_contiguous
from gerrychain.proposals import propose_random_flip
from gerrychain.accept import always_accept


def main() -> None:
    graph = Graph.from_json("temp/PA_VTDs.json")

    election = Election("SEN12", {"Dem": "USS12D", "Rep": "USS12R"})

    initial_partition = Partition(
        graph,
        assignment="CD_2011",
        updaters={
            "cut_edges": cut_edges,
            "population": Tally("TOTPOP", alias="population"),
            "SEN12": election,
        },
    )

    for district, pop in initial_partition["population"].items():
        print("District {}: {}".format(district, pop))

    chain = MarkovChain(
        proposal=propose_random_flip,
        constraints=[single_flip_contiguous],
        accept=always_accept,
        initial_state=initial_partition,
        total_steps=1000,
    )

    for link in chain:
        partition: Partition | None = link
        assert partition is not None
        print(sorted(partition["SEN12"].percents("Dem")))

    pass


if __name__ == "__main__":
    main()

### END ###
