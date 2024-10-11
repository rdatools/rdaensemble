# rdaensemble/general/__init__.py

from .compactness import cuts_and_boundaries
from .score import (
    score_ensemble,
    InferredVotes,
    is_same_candidate_preferred,
    is_defined_opportunity_district,
    count_defined_opportunity_districts,
    load_EI_votes,
    aggregate_votes_by_district,
)
from .notable_maps import (
    id_notable_maps,
    ratings_dimensions,
    ratings_indexes,
    better_map,
    qualifying_map,
)
from .metautils import shared_metadata, ensemble_metadata, scores_metadata
from .utils import make_plan, plan_from_ensemble

name: str = "general"
