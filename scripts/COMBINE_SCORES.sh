#!/bin/bash
#
# Combine the scores from the original ensemble and the pushed plans
#
# For example:
#
# scripts/COMBINE_SCORES.sh NC C
# scripts/COMBINE_SCORES.sh NC U -upper
# scripts/COMBINE_SCORES.sh NC L -lower

XX=$1
TYPECHAR=$2
TYPEDIR=$3
WORKING_DIR=../../iCloud/fileout/tradeoffs/${XX}/ensembles${TYPEDIR}

tail -n +2 $WORKING_DIR/${XX}20${TYPECHAR}_scores_optimized.csv > $WORKING_DIR/scores.tmp 
cat $WORKING_DIR/${XX}20${TYPECHAR}_scores.csv $WORKING_DIR/scores.tmp > $WORKING_DIR/${XX}20${TYPECHAR}_scores_augmented.csv
rm $WORKING_DIR/scores.tmp
