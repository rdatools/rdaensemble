#!/usr/bin/env python3

"""
MAKE A 'RANDOM' MAP FOR EACH STATE & PLAN TYPE COMBINATION

To run:

$ scripts/make_random_maps.py

scripts/rmfrst_ensemble.py \
    --data ../rdabase/data/NC/NC_2020_data.csv \
    --shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
    --graph ../rdabase/data/NC/NC_2020_graph.json \
    --log temp/NC20C_100_log.txt \
    --no-debug

scripts/random_map.py \
--state NC \
--plantype lower \
--roughlyequal 0.10 \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--output temp/NC20L_random_plan.csv \
--log temp/NC20L_random_log.txt \
--no-debug

"""

from typing import List, Dict

import os

from rdabase import DISTRICTS_BY_STATE

states_with_data: List[str] = [
    "AL",
    "AZ",
    "FL",
    "GA",
    "IL",
    "IN",
    "MD",
    "MI",
    "NC",
    "NJ",
    "NM",
    "OH",
    "PA",
    "SC",
    "TX",
    "VA",
    "WI",
]

mmd: Dict[str, List[str]] = {"MD": ["lower"]}

for xx, districts_by_type in DISTRICTS_BY_STATE.items():
    comment: str = "" if xx in states_with_data else "# "
    for plan_type, ndistricts in districts_by_type.items():
        if ndistricts is None or ndistricts == 1:
            continue

        if xx in mmd and plan_type in mmd[xx]:
            continue

        roughly_equal: float = 0.01 if plan_type == "congress" else 0.10
        prefix: str = f"{xx}20{plan_type[0].upper()}"

        command: str = f"echo 'Running {xx} {plan_type} {ndistricts} ...'"
        print(command)

        command: str = (
            f"{comment}scripts/random_map.py --state {xx} --plantype {plan_type} --roughlyequal {roughly_equal} --data ../rdabase/data/{xx}/{xx}_2020_data.csv --shapes ../rdabase/data/{xx}/{xx}_2020_shapes_simplified.json --graph ../rdabase/data/{xx}/{xx}_2020_graph.json --output temp/{prefix}_random_plan.csv --log temp/{prefix}_random_log.txt --no-debug"
        )
        print(command)
        # os.system(command)

### END ###
