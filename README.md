# rdaensemble

Redistricting ensembles

## Methods

This project supports several methods for generating ensembles of redistricting plans:

- Random maps from random spanning trees (RMfRST)
- Random maps from random starting points (RMfRSP)
- ReCom -- TODO
- Sequential Monte Carlo (SMC) -- TODO

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
[rdabase](https://github.com/rdatools/rdabase)
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

There is also a companion JSON file with metadata about the scores.

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
