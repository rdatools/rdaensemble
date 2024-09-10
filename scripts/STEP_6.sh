#!/bin/bash

# Default values
STATE=""
PLAN_TYPE=""
ROUGHLY_EQUAL=""

# Function to print usage
usage() {
    echo "Usage: $0 --state <STATE> --plan-type <PLAN_TYPE>"
    echo "  --state     : State abbreviation (e.g., $STATE)"
    echo "  --plan-type : Plan type (e.g., congress, upper, lower)"
    exit 1
}

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --state) STATE="$2"; shift ;;
        --plan-type) PLAN_TYPE="$2"; shift ;;
        *) echo "Unknown parameter: $1"; usage ;;
    esac
    shift
done

# Check if all required parameters are provided
if [ -z "$STATE" ] || [ -z "$PLAN_TYPE" ]; then
    echo "Error: Missing required parameters."
    usage
fi

# Derive additional values

ENSEMBLES_DIR="ensembles-${PLAN_TYPE}"
if [ "$PLAN_TYPE" = "congress" ]; then
    ENSEMBLES_DIR="ensembles"
fi

LETTER="${PLAN_TYPE:0:1}"
SUFFIX=`echo "${LETTER}" | tr '[a-z]' '[A-Z]'`
PREFIX="${STATE}20${SUFFIX}"

ROUGHLY_EQUAL=0.01
ROUGHLY_EQUAL_HALF=0.01
if [ "$PLAN_TYPE" = "upper" ] || [ "$PLAN_TYPE" = "lower" ]; then
    ROUGHLY_EQUAL=$ROUGHLY_EQUAL
    ROUGHLY_EQUAL_HALF=0.05
fi

# From 'rdaensemble'
# Optimize along each ratings dimension, combine the better plans into another ensemble, and score it.
# Combine the unbiased and optimized ratings, and find the new pairwise ratings frontiers.
# Finally, identify the notable maps in the augmented ensemble.

echo "Optimizing for proportionality ..."
scripts/recom_ensemble_optimized.py \
--state $STATE \
--size 10000 \
--roughlyequal $ROUGHLY_EQUAL \
--optimize proportionality \
--data ../rdabase/data/$STATE/${STATE}_2020_data.csv \
--shapes ../rdabase/data/$STATE/${STATE}_2020_shapes_simplified.json \
--graph ../rdabase/data/$STATE/${STATE}_2020_graph.json \
--plans ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_plans_optimized_proportionality.json \
--no-debug

echo "Optimizing for competitiveness ..."
scripts/recom_ensemble_optimized.py \
--state $STATE \
--size 10000 \
--roughlyequal $ROUGHLY_EQUAL \
--optimize competitiveness \
--data ../rdabase/data/$STATE/${STATE}_2020_data.csv \
--shapes ../rdabase/data/$STATE/${STATE}_2020_shapes_simplified.json \
--graph ../rdabase/data/$STATE/${STATE}_2020_graph.json \
--plans ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_plans_optimized_competitiveness.json \
--no-debug

echo "Optimizing for minority representation ..."
scripts/recom_ensemble_optimized.py \
--state $STATE \
--size 10000 \
--roughlyequal $ROUGHLY_EQUAL \
--optimize minority \
--data ../rdabase/data/$STATE/${STATE}_2020_data.csv \
--shapes ../rdabase/data/$STATE/${STATE}_2020_shapes_simplified.json \
--graph ../rdabase/data/$STATE/${STATE}_2020_graph.json \
--plans ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_plans_optimized_minority.json \
--no-debug

echo "Optimizing for compactness ..."
scripts/recom_ensemble_optimized.py \
--state $STATE \
--size 10000 \
--roughlyequal $ROUGHLY_EQUAL \
--optimize compactness \
--data ../rdabase/data/$STATE/${STATE}_2020_data.csv \
--shapes ../rdabase/data/$STATE/${STATE}_2020_shapes_simplified.json \
--graph ../rdabase/data/$STATE/${STATE}_2020_graph.json \
--plans ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_plans_optimized_compactness.json \
--no-debug

echo "Optimizing for splitting ..."
scripts/recom_ensemble_optimized.py \
--state $STATE \
--size 10000 \
--roughlyequal $ROUGHLY_EQUAL \
--optimize splitting \
--data ../rdabase/data/$STATE/${STATE}_2020_data.csv \
--shapes ../rdabase/data/$STATE/${STATE}_2020_shapes_simplified.json \
--graph ../rdabase/data/$STATE/${STATE}_2020_graph.json \
--plans ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_plans_optimized_splitting.json \
--no-debug

echo "Combining the optimized ensembles ..."
scripts/combine_ensembles.py \
--ensembles ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_plans_optimized_proportionality.json \
            ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_plans_optimized_competitiveness.json \
            ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_plans_optimized_minority.json \
            ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_plans_optimized_compactness.json \
            ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_plans_optimized_splitting.json \
--output ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_plans_optimized.json \
--no-debug

echo "Scoring the optimized ensemble ..."
scripts/score_ensemble.py \
--state $STATE \
--plans ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_plans_optimized.json \
--data ../rdabase/data/$STATE/${STATE}_2020_data.csv \
--shapes ../rdabase/data/$STATE/${STATE}_2020_shapes_simplified.json \
--graph ../rdabase/data/$STATE/${STATE}_2020_graph.json \
--scores ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_scores_optimized.csv \
--no-debug

echo "Combining the scores ..."
scripts/COMBINE_SCORES.sh $STATE U -${PLAN_TYPE}

echo "Finding the notable maps in the augmented ensemble ..."
scripts/id_notable_maps.py \
--scores ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_scores_augmented.csv \
--metadata ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_scores_metadata.json \
--notables ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_notable_maps.json \
--no-debug

### END ###
