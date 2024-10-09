#!/usr/bin/env python3

"""
TEST CALCULATION OF MINORITY OPPORTUNITY DISTRICTS
"""

from rdaensemble.general import (
    is_defined_opportunity_district,
    InferredVotes,
    count_defined_opportunity_districts,
)


class TestMinorityOpportunity:
    """Test detection of minority opportunity districts."""

    def test_is_defined_opportunity_district(self) -> None:
        """Test the function is_defined_opportunity_district()."""

        # The district is a minority opportunity district, D preferred
        result: bool = is_defined_opportunity_district(
            dem_votes=100,
            rep_votes=50,
            group_dem_votes=45,
            group_rep_votes=5,
            other_dem_votes=40,
            other_rep_votes=60,
        )
        assert result is True

        # The district is a minority opportunity district, R preferred
        result: bool = is_defined_opportunity_district(
            dem_votes=50,
            rep_votes=100,
            group_dem_votes=5,
            group_rep_votes=45,
            other_dem_votes=60,
            other_rep_votes=40,
        )
        assert result is True

        # The district is NOT a minority opportunity district
        # The minority-preferred candidate (D) DIDN'T win the district
        result: bool = is_defined_opportunity_district(
            dem_votes=70,
            rep_votes=80,
            group_dem_votes=45,
            group_rep_votes=5,
            other_dem_votes=25,
            other_rep_votes=75,
        )
        assert result is False

        # The district is NOT a minority opportunity district
        # The minority-preferred candidate (R) DIDN'T win the district
        result: bool = is_defined_opportunity_district(
            dem_votes=80,
            rep_votes=70,
            group_dem_votes=5,
            group_rep_votes=45,
            other_dem_votes=75,
            other_rep_votes=25,
        )
        assert result is False

        # The district is NOT a minority opportunity district
        # The minority group votes for the preferred candidate (D) DON'T outnumber the white+other votes for the preferred candidate
        result: bool = is_defined_opportunity_district(
            dem_votes=100,
            rep_votes=50,
            group_dem_votes=40,
            group_rep_votes=10,
            other_dem_votes=60,
            other_rep_votes=50,
        )
        assert result is False

        # The district is NOT a minority opportunity district
        # The minority group votes for the preferred candidate (R) DON'T outnumber the white+other votes for the preferred candidate
        result: bool = is_defined_opportunity_district(
            dem_votes=50,
            rep_votes=100,
            group_dem_votes=10,
            group_rep_votes=40,
            other_dem_votes=40,
            other_rep_votes=60,
        )
        assert result is False

    def test_count_defined_opportunity_districts(self) -> None:

        districts_EI: list[InferredVotes] = [
            InferredVotes(
                dem_votes=135,
                rep_votes=65,
                black_dem_votes=45,
                black_rep_votes=5,
                hispanic_dem_votes=35,
                hispanic_rep_votes=15,
                other_dem_votes=40,
                other_rep_votes=60,
            ),  # Black opportunity district
            InferredVotes(
                dem_votes=135,
                rep_votes=65,
                black_dem_votes=35,
                black_rep_votes=15,
                hispanic_dem_votes=45,
                hispanic_rep_votes=5,
                other_dem_votes=40,
                other_rep_votes=60,
            ),  # Hispanic opportunity district
            InferredVotes(
                dem_votes=70,
                rep_votes=80,
                black_dem_votes=45,
                black_rep_votes=5,
                hispanic_dem_votes=0,
                hispanic_rep_votes=0,
                other_dem_votes=25,
                other_rep_votes=75,
            ),  # D's didn't win the district
            InferredVotes(
                dem_votes=50,
                rep_votes=100,
                black_dem_votes=0,
                black_rep_votes=0,
                hispanic_dem_votes=10,
                hispanic_rep_votes=40,
                other_dem_votes=40,
                other_rep_votes=60,
            ),  # Hispanic votes don't outnumber white+other votes
        ]
        actual: int = count_defined_opportunity_districts(districts_EI)
        expected: int = 2
        assert actual == expected

        assert True


### END ###
