# rdaensemble

Redistricting ensembles

## Methods

The code in this repository supports several methods for generating ensembles of redistricting plans (maps):

- Random maps from random spanning trees (RMfRST)
- Random maps from random starting points (RMfRSP)
- Ensemble of maps using MCMC/ReCom (ReCom)
- Ensemble of maps using Sequential Monte Carlo (SMC) <<< TODO

## Input Files

The inputs for generating &amp; scoring ensembles are:

```python
from rdascore import load_data, load_shapes, load_graph, load_metadata

data: Dict[str, Dict[str, int | str]] = load_data(data_path)
shapes: Dict[str, Any] = load_shapes(shapes_path)
graph: Dict[str, List[str]] = load_graph(graph_path)
metadata: Dict[str, Any] = load_metadata(state_code, data_path)
```

The precinct data, shapes, and graphs are all available in the companion repository
[rdatools/rdabase](https://github.com/rdatools/rdabase)
in the `data` directory by state.
They are named `NC_2020_data.csv`, `NC_2020_shapes_simplified.json`, and `NC_2020_graph.json`,
for example.

Theoretically, these inputs can come from any source, but for simplicity, reproducibility, and apples-to-apples comparisons,
it's best to use the input files in `rdabase`.
  
## Output Files

Ensembles are saved as JSON files.
A file contains metadata about the ensemble, including the method used to generate it,
and then a `plans` key with a list of plans:

```python
plans: List[Dict[str, str | float | Dict[str, int | str]]]
```

Each plan item has a `name` (`str`), an optional `weight` (`float`), and a
`plan` (`Dict[str, int | str]]`) which represents the assignments as 
geoid: district_id key: value pairs.

Scores for the plans in an ensemble are saved as a CSV file,
with one row per plan and one column per metric.
The metrics are the same as those produced by 
[rdatools/rdascore](https://github.com/rdatools/rdascore),
except they also include the energy of the plan.
The metric names are descriptive.

When a scores CSV file is produced, a companion JSON file with metadata about the scoring is also generated.

## Naming Conventions

You can name ensemble and score files anything you want.
To facilitate understanding the contents of these files without having to open them, 
we recommend the following the convention:

- Ensemble example: `NC20C_RMfRST_1000_plans.json`
- Scores example: `NC20C_RMfRST_1000_scores.csv`

where "NC" is the state code, "20" stands for the 2020 census cycle, 
"C" abbreviates "Congress" (as opposed to state upper or lower house), 
"RMfRST" is the method, 1000 is the number of plans in the ensemble, and 
"plans" and "scores" distinguish between the two types of files.

Note: The scores metadata file will be named the same as the scores file,
except it will end `_metadata.json` instead of `.csv`, 
for example, `NC20C_RMfRST_1000_scores_metadata.json`.

## Usage

To generate an ensemble of 1,000 plans using the random maps from random spanning trees method (RMfRST), run:

```bash
scripts/rmfrst_ensemble.py \
--state NC \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--size 1000 \
--plans ~/iCloud/fileout/ensembles/NC20C_RMfRST_1000_plans.json \
--log ~/iCloud/fileout/ensembles/NC20C_RMfRST_1000_log.txt \
--no-debug
```

To score the resulting ensemble, run:

```bash
scripts/score_ensemble.py \
--state NC \
--plans ~/iCloud/fileout/ensembles/NC20C_RMfRST_1000_plans.json \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--scores ~/iCloud/fileout/ensembles/NC20C_RMfRST_1000_scores.csv \
--no-debug
```

To generate random maps from random starting points (RMfRSP) instead, use the `rmfrst_ensemble.py` script.
For ReCom, use the `recom_ensemble.py` script.

Note: Ensemble JSON files can be quite large, bigger than GitHub's 100 MB file size limit,
so we recommend that you write them to the `ensembles` directory, which is ignored by Git.