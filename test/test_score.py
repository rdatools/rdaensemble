#!/usr/bin/env python3

"""
TEST CALCULATION OF MINORITY OPPORTUNITY DISTRICTS
"""

from rdaensemble.general import (
    InferredVotes,
    is_same_candidate_preferred,
    is_defined_opportunity_district,
    count_defined_opportunity_districts,
)


class TestMinorityOpportunity:
    """Test detection of minority opportunity districts."""

    def test_is_defined_opportunity_district(self) -> None:
        """Test the function is_defined_opportunity_district()."""

        # The district is a minority opportunity district, D preferred
        result: bool = is_defined_opportunity_district(
            dem_votes=65,
            rep_votes=55,
            group_dem_votes=35,
            group_rep_votes=5,
            other_dem_votes=25,
            other_rep_votes=35,
        )
        assert result is True

        # The district is a minority opportunity district, R preferred
        result: bool = is_defined_opportunity_district(
            dem_votes=55,
            rep_votes=65,
            group_dem_votes=5,
            group_rep_votes=35,
            other_dem_votes=35,
            other_rep_votes=25,
        )
        assert result is True

        # The district is NOT a minority opportunity district
        # The minority-preferred candidate (D) DIDN'T win the district
        result: bool = is_defined_opportunity_district(
            dem_votes=55,
            rep_votes=65,
            group_dem_votes=35,
            group_rep_votes=5,
            other_dem_votes=15,
            other_rep_votes=40,
        )
        assert result is False

        # The district is NOT a minority opportunity district
        # The minority-preferred candidate (R) DIDN'T win the district
        result: bool = is_defined_opportunity_district(
            dem_votes=65,
            rep_votes=55,
            group_dem_votes=5,
            group_rep_votes=35,
            other_dem_votes=40,
            other_rep_votes=15,
        )
        assert result is False

        # The district is NOT a minority opportunity district
        # The minority group votes for the preferred candidate (D) DON'T outnumber the white+other votes for the preferred candidate
        result: bool = is_defined_opportunity_district(
            dem_votes=65,
            rep_votes=55,
            group_dem_votes=30,
            group_rep_votes=5,
            other_dem_votes=35,
            other_rep_votes=30,
        )
        assert result is False

        # The district is NOT a minority opportunity district
        # The minority group votes for the preferred candidate (R) DON'T outnumber the white+other votes for the preferred candidate
        result: bool = is_defined_opportunity_district(
            dem_votes=55,
            rep_votes=65,
            group_dem_votes=5,
            group_rep_votes=30,
            other_dem_votes=30,
            other_rep_votes=35,
        )
        assert result is False

    def test_is_same_candidate_preferred(self) -> None:
        """Test the function is_same_candidate_preferred()."""

        actual: bool = is_same_candidate_preferred(
            black_dem_votes=30,
            black_rep_votes=20,
            hispanic_dem_votes=20,
            hispanic_rep_votes=30,
        )
        assert not actual

        actual: bool = is_same_candidate_preferred(
            black_dem_votes=30,
            black_rep_votes=20,
            hispanic_dem_votes=20,
            hispanic_rep_votes=10,
        )
        assert actual

    def test_count_defined_opportunity_districts(self) -> None:
        """Test the function count_defined_opportunity_districts()."""

        districts_EI: list[InferredVotes] = [
            InferredVotes(
                dem_votes=65,
                rep_votes=55,
                black_dem_votes=35,
                black_rep_votes=5,
                hispanic_dem_votes=5,
                hispanic_rep_votes=20,
                other_dem_votes=25,
                other_rep_votes=30,
            ),  # Black opportunity district
            InferredVotes(
                dem_votes=65,
                rep_votes=55,
                black_dem_votes=5,
                black_rep_votes=20,
                hispanic_dem_votes=35,
                hispanic_rep_votes=5,
                other_dem_votes=25,
                other_rep_votes=30,
            ),  # Hispanic opportunity district
            InferredVotes(
                dem_votes=55,
                rep_votes=65,
                black_dem_votes=35,
                black_rep_votes=5,
                hispanic_dem_votes=5,
                hispanic_rep_votes=20,
                other_dem_votes=15,
                other_rep_votes=40,
            ),  # D's didn't win the district
            InferredVotes(
                dem_votes=65,
                rep_votes=55,
                black_dem_votes=30,
                black_rep_votes=5,
                hispanic_dem_votes=0,
                hispanic_rep_votes=20,
                other_dem_votes=35,
                other_rep_votes=30,
            ),  # Black votes don't outnumber white+other votes
            InferredVotes(
                dem_votes=65,
                rep_votes=55,
                black_dem_votes=25,
                black_rep_votes=5,
                hispanic_dem_votes=15,
                hispanic_rep_votes=10,
                other_dem_votes=25,
                other_rep_votes=40,
            ),  # Coalition opportunity district
            InferredVotes(
                dem_votes=65,
                rep_votes=55,
                black_dem_votes=15,
                black_rep_votes=5,
                hispanic_dem_votes=15,
                hispanic_rep_votes=10,
                other_dem_votes=35,
                other_rep_votes=40,
            ),  # Not a Coalition opportunity district
        ]
        actual: int = count_defined_opportunity_districts(districts_EI)
        expected: int = 3
        assert actual == expected

        assert True


### END ###
