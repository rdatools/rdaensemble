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

        # AN OPPORTUNITY DISTRICT, D PREFERRED

        # D's won the district
        dem_votes: int = 100
        rep_votes: int = 50

        # The minority group preferred the D candidate
        group_dem_votes: int = 45
        group_rep_votes: int = 5

        # The minority group votes for the preferred candidate outnumber the white+other votes for the preferred candidate
        white_dem_votes: int = 40
        white_rep_votes: int = 60

        # Test the function
        result: bool = is_defined_opportunity_district(
            dem_votes=dem_votes,
            rep_votes=rep_votes,
            group_dem_votes=group_dem_votes,
            group_rep_votes=group_rep_votes,
            other_dem_votes=white_dem_votes,
            other_rep_votes=white_rep_votes,
        )

        # The district is a minority opportunity district
        assert result is True

        # AN OPPORTUNITY DISTRICT, R PREFERRED

        # D's won the district
        dem_votes: int = 50
        rep_votes: int = 100

        # The minority group preferred the D candidate
        group_dem_votes: int = 5
        group_rep_votes: int = 45

        # The minority group votes for the preferred candidate outnumber the white+other votes for the preferred candidate
        white_dem_votes: int = 60
        white_rep_votes: int = 40

        # Test the function
        result: bool = is_defined_opportunity_district(
            dem_votes=dem_votes,
            rep_votes=rep_votes,
            group_dem_votes=group_dem_votes,
            group_rep_votes=group_rep_votes,
            other_dem_votes=white_dem_votes,
            other_rep_votes=white_rep_votes,
        )

        # The district is a minority opportunity district
        assert result is True

        # NOT AN OPPORTUNITY DISTRICT

        # D's DIDN'T win the district
        dem_votes: int = 70
        rep_votes: int = 80

        # The minority group preferred the D candidate
        group_dem_votes: int = 45
        group_rep_votes: int = 5

        # The minority group votes for the preferred candidate outnumber the white+other votes for the preferred candidate
        white_dem_votes: int = 25
        white_rep_votes: int = 75

        # Test the function
        result: bool = is_defined_opportunity_district(
            dem_votes=dem_votes,
            rep_votes=rep_votes,
            group_dem_votes=group_dem_votes,
            group_rep_votes=group_rep_votes,
            other_dem_votes=white_dem_votes,
            other_rep_votes=white_rep_votes,
        )

        # The district is NOT a minority opportunity district
        assert result is False

        # NOT AN OPPORTUNITY DISTRICT

        # R's DIDN'T win the district
        dem_votes: int = 80
        rep_votes: int = 70

        # The minority group preferred the D candidate
        group_dem_votes: int = 5
        group_rep_votes: int = 45

        # The minority group votes for the preferred candidate outnumber the white+other votes for the preferred candidate
        white_dem_votes: int = 75
        white_rep_votes: int = 25

        # Test the function
        result: bool = is_defined_opportunity_district(
            dem_votes=dem_votes,
            rep_votes=rep_votes,
            group_dem_votes=group_dem_votes,
            group_rep_votes=group_rep_votes,
            other_dem_votes=white_dem_votes,
            other_rep_votes=white_rep_votes,
        )

        # The district is NOT a minority opportunity district
        assert result is False

        # NOT AN OPPORTUNITY DISTRICT

        # D's won the district
        dem_votes: int = 100
        rep_votes: int = 50

        # The minority group preferred the D candidate
        group_dem_votes: int = 40
        group_rep_votes: int = 10

        # The minority group votes for the preferred candidate DON'T outnumber the white+other votes for the preferred candidate
        white_dem_votes: int = 60
        white_rep_votes: int = 40

        # Test the function
        result: bool = is_defined_opportunity_district(
            dem_votes=dem_votes,
            rep_votes=rep_votes,
            group_dem_votes=group_dem_votes,
            group_rep_votes=group_rep_votes,
            other_dem_votes=white_dem_votes,
            other_rep_votes=white_rep_votes,
        )

        # The district is NOT a minority opportunity district
        assert result is False

        # NOT AN OPPORTUNITY DISTRICT

        # DR's won the district
        dem_votes: int = 50
        rep_votes: int = 100

        # The minority group preferred the R candidate
        group_dem_votes: int = 10
        group_rep_votes: int = 40

        # The minority group votes for the preferred candidate DON'T outnumber the white+other votes for the preferred candidate
        white_dem_votes: int = 40
        white_rep_votes: int = 60

        # Test the function
        result: bool = is_defined_opportunity_district(
            dem_votes=dem_votes,
            rep_votes=rep_votes,
            group_dem_votes=group_dem_votes,
            group_rep_votes=group_rep_votes,
            other_dem_votes=white_dem_votes,
            other_rep_votes=white_rep_votes,
        )

        # The district is NOT a minority opportunity district
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
