#!/usr/bin/env python3

"""
TEST CALCULATION OF MINORITY OPPORTUNITY DISTRICTS
"""

import random

from rdaensemble.general import is_defined_opportunity_district


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
            white_dem_votes=white_dem_votes,
            white_rep_votes=white_rep_votes,
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
            white_dem_votes=white_dem_votes,
            white_rep_votes=white_rep_votes,
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
            white_dem_votes=white_dem_votes,
            white_rep_votes=white_rep_votes,
        )

        # The district is NOT a minority opportunity district
        assert result is False


### END ###
