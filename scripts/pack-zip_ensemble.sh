#!/bin/bash
#
# Pack & zip an ensemble, so it can be put into a GitHub repository.
#
# For example:
#
# scripts/pack-zip_ensemble.sh --state NC --plantype congress
#

# Initialize variables
state=""
plantype=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --state)
            state="$2"
            shift 2
            ;;
        --plantype)
            plantype="$2"
            shift 2
            ;;
        *)
            echo "Unknown parameter: $1"
            exit 1
            ;;
    esac
done

# Check if all required parameters are provided
if [[ -z $state || -z $plantype ]]; then
    echo "Error: All parameters (--state, --plantype) are required."
    echo "Usage: $0 --state <state> --plantype <plantype>"
    exit 1
fi

letter="${plantype:0:1}"
suffix=`echo "${letter}" | tr '[a-z]' '[A-Z]'`
prefix="${state}20${suffix}"

echo "Packing ensemble ..."
scripts/pack_ensemble.py --input ../../iCloud/fileout/tradeoffs/$state/ensembles/${prefix}_plans.json --output temp/${prefix}_plans_packed.json --no-debug

echo "Zipping the packed ensemble ..."
zip -9q ../tradeoffs-dropbox/ensembles/${prefix}_plans_packed.json.zip temp/${prefix}_plans_packed.json

echo "Cleaning up ..."
rm temp/${prefix}_plans_packed.json