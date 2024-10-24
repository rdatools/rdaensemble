"""
MINORITY OPPORTUNITY DISTRICTS (FORMALLY DEFINED)
"""

from typing import List, Dict, Tuple, NamedTuple

from collections import defaultdict, OrderedDict


from rdabase import (
    Assignment,
    read_csv,
)


class InferredVotes(NamedTuple):
    """Votes inferred from the total votes and the votes of a group."""

    dem_votes: int
    rep_votes: int
    black_dem_votes: int
    black_rep_votes: int
    hispanic_dem_votes: int
    hispanic_rep_votes: int
    other_dem_votes: int
    other_rep_votes: int


def is_same_candidate_preferred(
    black_dem_votes: int,
    black_rep_votes: int,
    hispanic_dem_votes: int,
    hispanic_rep_votes: int,
) -> bool:
    """Do Blacks and Hispanic prefer the same candidate?"""

    return (
        (black_dem_votes > black_rep_votes)
        and (hispanic_dem_votes > hispanic_rep_votes)
    ) or (
        (black_dem_votes < black_rep_votes)
        and (hispanic_dem_votes < hispanic_rep_votes)
    )

    return True


def is_defined_opportunity_district(
    dem_votes: int,
    rep_votes: int,
    group_dem_votes: int,
    group_rep_votes: int,
    other_dem_votes: int,
    other_rep_votes: int,
) -> bool:
    """Is a district a defined minority opportunity district?

    Parameters:
    dem_votes: int - Democratic votes in the district
    rep_votes: int - Republican votes in the district
    group_dem_votes: int - Democratic votes in the minority group (e.g., Black or Hispanic) in the district
    group_rep_votes: int - Republican votes in the minority group in the district
    other_dem_votes: int - Democratic votes in the white + other group in the district
    other_rep_votes: int - Republican votes in the white + other group in the district

    Returns:
    bool - True if the district is defined as a minority opportunity district, False otherwise

    """

    # The minority-preferred candidate is one who received a majority of the minority group's votes
    minority_preferred_candidate_is_dem: bool = group_dem_votes > group_rep_votes

    # Two conditions must be met for a district to be a defined minority opportunity district:
    # 1 - The minority preferred candidate must win the district
    minority_preferred_candidate_won: bool = (
        minority_preferred_candidate_is_dem and dem_votes > rep_votes
    ) or (not minority_preferred_candidate_is_dem and rep_votes > dem_votes)

    # 2 - The minority group votes for the preferred candidate must outnumber the white+other votes for the preferred candidate
    minority_votes_outnumber_other_votes: bool = (
        minority_preferred_candidate_is_dem and group_dem_votes > other_dem_votes
    ) or (not minority_preferred_candidate_is_dem and group_rep_votes > other_rep_votes)

    return minority_preferred_candidate_won and minority_votes_outnumber_other_votes


def count_defined_opportunity_districts(
    votes_by_district: List[InferredVotes],
) -> Tuple[int, List[int | str]]:
    """Count the number of defined Black & Hispanic opportunity districts in a set of districts."""

    count: int = 0
    mods: List[int | str] = list()

    for i, votes in enumerate(votes_by_district):
        j: int = i + 1

        scenario_1: bool = is_defined_opportunity_district(
            votes.dem_votes,
            votes.rep_votes,
            votes.black_dem_votes,
            votes.black_rep_votes,
            votes.other_dem_votes,
            votes.other_rep_votes,
        )  # Black opportunity district
        scenario_2: bool = is_defined_opportunity_district(
            votes.dem_votes,
            votes.rep_votes,
            votes.hispanic_dem_votes,
            votes.hispanic_rep_votes,
            votes.other_dem_votes,
            votes.other_rep_votes,
        )  # Hispanic opportunity district
        scenario_3: bool = is_same_candidate_preferred(
            votes.black_dem_votes,
            votes.black_rep_votes,
            votes.hispanic_dem_votes,
            votes.hispanic_rep_votes,
        ) and is_defined_opportunity_district(
            votes.dem_votes,
            votes.rep_votes,
            votes.black_dem_votes + votes.hispanic_dem_votes,
            votes.black_rep_votes + votes.hispanic_rep_votes,
            votes.other_dem_votes,
            votes.other_rep_votes,
        )  # Coalition opportunity district

        if scenario_1 or scenario_2 or scenario_3:
            count += 1
            mods.append(j)

    return count, mods


def load_EI_votes(votes_file: str) -> Dict[str, InferredVotes]:
    """Read an EI estimated votes file."""

    fields: List[str] = [
        "pre_20_rep_white",
        "pre_20_rep_black",
        "pre_20_rep_hisp",
        "pre_20_rep_oth",
        "pre_20_dem_white",
        "pre_20_dem_black",
        "pre_20_dem_hisp",
        "pre_20_dem_oth",
    ]
    field_types = [str] + [int] * len(fields)

    raw_by_precinct: List[Dict[str, int | str]] = read_csv(votes_file, field_types)

    estimates_by_precinct: Dict[str, InferredVotes] = dict()
    for row in raw_by_precinct:
        geoid: str = str(row["GEOID"])
        rep_white: int = int(row["pre_20_rep_white"])
        rep_black: int = int(row["pre_20_rep_black"])
        rep_hisp: int = int(row["pre_20_rep_hisp"])
        rep_oth: int = int(row["pre_20_rep_oth"])
        dem_white: int = int(row["pre_20_dem_white"])
        dem_black: int = int(row["pre_20_dem_black"])
        dem_hisp: int = int(row["pre_20_dem_hisp"])
        dem_oth: int = int(row["pre_20_dem_oth"])
        estimated_votes: InferredVotes = InferredVotes(
            dem_votes=dem_white + dem_black + dem_hisp + dem_oth,
            rep_votes=rep_white + rep_black + rep_hisp + rep_oth,
            black_dem_votes=dem_black,
            black_rep_votes=rep_black,
            hispanic_dem_votes=dem_hisp,
            hispanic_rep_votes=rep_hisp,
            other_dem_votes=dem_white + dem_oth,
            other_rep_votes=rep_white + rep_oth,
        )
        estimates_by_precinct[geoid] = estimated_votes

    return estimates_by_precinct


def aggregate_votes_by_district(
    assignments: List[Assignment],
    votes: Dict[str, InferredVotes],
    n_districts: int,
) -> Dict[int | str, InferredVotes]:
    """Aggregate EI-estimated votes by district."""

    aggregate: List[Dict[int | str, int]] = [
        defaultdict(int) for _ in range(n_districts + 1)
    ]

    for a in assignments:
        # NOTE - Generalize this for str districts
        aggregate[int(a.district)]["dem_votes"] += votes[a.geoid].dem_votes
        aggregate[int(a.district)]["rep_votes"] += votes[a.geoid].rep_votes
        aggregate[int(a.district)]["black_dem_votes"] += votes[a.geoid].black_dem_votes
        aggregate[int(a.district)]["black_rep_votes"] += votes[a.geoid].black_rep_votes
        aggregate[int(a.district)]["hispanic_dem_votes"] += votes[
            a.geoid
        ].hispanic_dem_votes
        aggregate[int(a.district)]["hispanic_rep_votes"] += votes[
            a.geoid
        ].hispanic_rep_votes
        aggregate[int(a.district)]["other_dem_votes"] += votes[a.geoid].other_dem_votes
        aggregate[int(a.district)]["other_rep_votes"] += votes[a.geoid].other_rep_votes

    by_district: Dict[int | str, InferredVotes] = {
        i: InferredVotes(
            dem_votes=d["dem_votes"],
            rep_votes=d["rep_votes"],
            black_dem_votes=d["black_dem_votes"],
            black_rep_votes=d["black_rep_votes"],
            hispanic_dem_votes=d["hispanic_dem_votes"],
            hispanic_rep_votes=d["hispanic_rep_votes"],
            other_dem_votes=d["other_dem_votes"],
            other_rep_votes=d["other_rep_votes"],
        )
        for i, d in enumerate(aggregate)
    }

    return by_district


### END ###
