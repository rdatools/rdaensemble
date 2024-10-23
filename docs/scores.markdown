# Scores (Metrics)

TODO - Update this.

These are the metrics ("scores") used in this analysis, in the order that they appear in the scores CSV.

The measures of partisan bias and responsiveness are described in some detail in
[Advanced Measures of Bias &amp; Responsiveness](https://medium.com/dra-2020/advanced-measures-of-bias-responsiveness-c1bf182d29a9).
Many use [fractional seat probabilities](https://lipid.phys.cmu.edu/nagle/Technical/FractionalSeats2.pdf).

The county and district splitting measures are described in
[Measuring County &amp; District Splitting](https://medium.com/dra-2020/measuring-county-district-splitting-48a075bcce39).

## General

*   **map** &ndash; The plan (map) name.
*   **energy** &ndash; The energy of the map. Lower is more *population* compact.
*   **cut_edges** &ndash; The percentage of edges between precincts that cross district boundaries.

*   **D** &ndash; The number of districts.
*   **C** &ndash; The number of counties.
*   **population_deviation** &ndash; The population deviation of the plan.
*   **estimated_vote_pct** &ndash; The Democratic two-party vote share.

## Partisan Bias

*   **pr_deviation** &ndash; The deviation from pr_seats. Smaller is better, and zero is perfect.
*   **pr_seats** &ndash; The integral number of seats closest to proportional representation.
*   **pr_pct** &ndash; pr_seats as a percentage of the number of districts.
*   **estimated_seats** &ndash; The estimated number of fractional Democratic seats.
*   **estimated_seat_pct** &ndash; estimated_seats as a percentage of the number of districts.
*   **fptp_seats** &ndash; The estimated number of Democratic seats using "first past the post" (FPTP), all-or-nothing accounting.
*   **disproportionality** &ndash; estimated_vote_pct minus estimated_seat_pct.
*   **efficiency_gap** &ndash; The efficiency gap. Smaller absolute value is better. Positive values favor Republicans; negative values favor Democrats.
*   **gamma** &ndash; A new measure of bias that combines seats and responsiveness.
*   **seats_bias** (αₛ) &ndash; The seats bias at 50% Democratic vote share.
*   **votes_bias** (αᵥ) &ndash; The votes bias at 50% Democratic vote share.
*   **geometric_seats_bias** (β) &ndash; The seats bias at the statewide Democratic vote share, not 50% (aka "partisan bias").
*   **global_symmetry** (GS) &ndash; A combination of seats and votes bias.
*   **declination** (δ) &ndash; The declination angle (in degrees), calculated using fractional seats and votes. Smaller is better.
*   **mean_median_statewide** &ndash; The statewide Democratic two-party vote share minus the median Democratic two-party district vote share.
*   **mean_median_average_district** &ndash; The mean Democratic two-party district vote share minus the median Democratic two-party district vote share.
*   **turnout_bias** (TO) &ndash; The difference between the statewide Democratic vote share and the average their average district vote share.
*   **lopsided_outcomes** (LO) &ndash; The difference between the average two-party vote shares for the Democratic and Republican wins.

## Competitiveness & Responsiveness

*   **competitive_districts** &ndash; The estimated number of competitive districts, using fractional seat probabilities.
*   **competitive_district_pct** &ndash; TODO.
*   **average_margin** &ndash; The average margin of victory.
*   **responsiveness** (ρ) &ndash; The slope of the seats-votes curve at the statewide Democratic vote share.
*   **responsive_districts** &ndash; The likely number of responsive districts, using fractional seat probabilities.
*   **responsive_district_pct** &ndash; responsive_districts as a percentage of the number of districts (D).
*   **overall_responsiveness** (R) &ndash; An overall measure of responsiveness which you can think of as a winner’s bonus.
*   **avg_dem_win_pct** &ndash; The average Democratic two-party vote share in districts won by Democrats.
*   **avg_rep_win_pct** &ndash; The average Republican two-party vote share in districts won by Republicans.

## Opportunity for Minority Representation

*   **opportunity_districts** &ndash; The estimated number of single race or ethnicity minority opportunity districts, using fractional seat probabilities.
*   **proportional_opportunities** &ndash; The proportional number of single race or ethnicity minority opportunity districts, based on statewide VAP.
*   **coalition_districts** &ndash; The estimated number of all-minorities-together coalition districts, using fractional seat probabilities.
*   **proportional_coalitions** &ndash; The proportional number of all-minorities-together coalition districts, based on statewide VAP.
*   **alt_opportunity_districts** &ndash; The estimated number of single race or ethnicity minority opportunity districts, using fractional seat probabilities. Unlike opportunity_districts, this "alt" metric means does not clip below the 37% threshold.
*   **alt_coalition_districts** &ndash; The estimated number of all-minorities-together coalition districts, using fractional seat probabilities. Unlike coalition_districts, this "alt" metric does not clip below the 37% threshold.
*   **defined_opportunity_districts** &ndash; The sum of minority opportunity districts for Blacks alone, Hispanics alone, and Blacks & Hispanics together, where a district is defined as a minority opportunity when the minority preferred candidate wins the district and there are more minority votes for the winner than white votes for the winner.

## Compactness -- TODO

*   **reock** &ndash; The average Reock measure of compactnes for the district shapes.
*   **polsby_popper** &ndash; The average Polsby-Popper measure of compactness for the district shapes.

## County-District Splitting

*   **county_splitting** &ndash; A measure of the degree of county splitting. Smaller is better, and 1.0 (no splitting) is the best.
*   **district_splitting** &ndash; A measure of the degree of district splitting. Smaller is better, and 1.0 (no splitting) is the best.
*   **counties_split** &ndash; The number of counties split across districts.
*   **county_splits** &ndash; The number of *times* counties are split, e.g, a county may be split into three or more pieces.
*   **proportionality** &ndash; DRA's propoprtionality rating. Integers [0-100], where bigger is better.

## Dave's Redistricting Ratings

*   **competitiveness** &ndash; DRA's competitiveness rating. Integers [0-100], where bigger is better.
*   **minority** &ndash; DRA's minority opportunity rating. Integers [0-100], where bigger is better.
*   **compactness** &ndash; DRA's compactness rating. Integers [0-100], where bigger is better.
*   **splitting** &ndash; DRA's county-district splitting rating. Integers [0-100], where bigger is better.