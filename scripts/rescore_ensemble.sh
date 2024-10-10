#!/bin/bash

# Default values
STATE=""
PLAN_TYPE=""

# Function to print usage
usage() {
    echo "Usage: $0 --state <STATE> --plantype <PLAN_TYPE>"
    echo "  --state     : State abbreviation (e.g., $STATE)"
    echo "  --plantype : Plan type (e.g., congress, upper, lower)"
    exit 1
}

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --state) STATE="$2"; shift ;;
        --plantype) PLAN_TYPE="$2"; shift ;;
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
if [ "$PLAN_TYPE" = "upper" ] || [ "$PLAN_TYPE" = "lower" ]; then
    ROUGHLY_EQUAL=0.10
fi

# From 'rdaensemble'
# Score an ensemble that has already been generated.

# echo "Generating an unbiased ensemble ..."
# scripts/recom_ensemble.py \
# --state $STATE \
# --plantype $PLAN_TYPE \
# --size 10000 \
# --roughlyequal $ROUGHLY_EQUAL \
# --root random_maps/${PREFIX}_random_plan.csv \
# --data ../rdabase/data/$STATE/${STATE}_2020_data.csv \
# --graph ../rdabase/data/$STATE/${STATE}_2020_graph.json \
# --plans ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_plans.json \
# --log ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_log.txt \
# --no-debug

echo "Scoring the unbiased ensemble ..."
scripts/score_ensemble.py \
--state $STATE \
--plantype $PLAN_TYPE \
--plans ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_plans.json \
--data ../rdabase/data/$STATE/${STATE}_2020_data.csv \
--shapes ../rdabase/data/$STATE/${STATE}_2020_shapes_simplified.json \
--graph ../rdabase/data/$STATE/${STATE}_2020_graph.json \
--scores ../../iCloud/fileout/tradeoffs/$STATE/$ENSEMBLES_DIR/${PREFIX}_scores.csv \
--no-debug

### END ###
