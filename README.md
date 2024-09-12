# rdaensemble

Redistricting ensembles

## Installation

To clone the repository:

```bash
$ git clone https://github.com/rdatools/rdaensemble
$ cd rdaensemble
```

To run the scripts, install the dependencies:

```bash
pip install -r requirements.txt
```

To install the package in another project:

```bash
$ pip install rdaensemble
```

## Usage

To generate an ensemble of plans, use one of the `*_ensemble.py` scripts:

* `rmfrst_ensemble.py` for Random Maps from Random Spanning Trees (RMfRST)
* `rmfrsp_ensemble.py` for Random Maps from Random Starting Points (RMfRSP)
* `recom_ensemble.py` for ReCom

There are example calls in each file.
Note: The resulting ensemble JSON files can be quite large--bigger than GitHub's 100 MB file size limit--
so we recommend that you write them to a directory which is not under source control.

To score the plans in an ensemble, use the `score_ensemble.py` script.

The other scripts are specific to our "trade-offs in redistricting" project and are not generally useful.

## Notes

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
