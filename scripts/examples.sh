# Generate & score 100-plan ensembles

scripts/rmfrst_ensemble.py \
--state NC \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--size 100 \
--plans output/NC20C_RMfRST_100_plans.json \
--log output/NC20C_RMfRST_100_log.txt \
--no-debug

scripts/score_ensemble.py \
--state NC \
--plans output/NC20C_RMfRST_100_plans.json \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--scores output/NC20C_RMfRST_100_scores.csv \
--no-debug

scripts/rmfrsp_ensemble.py \
--state NC \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--size 100 \
--plans output/NC20C_RMfRSP_100_plans.json \
--log output/NC20C_RMfRSP_100_log.txt \
--no-debug

# Score root map candidates

scripts/score_ensemble.py \
--state NC \
--plans ../rdaroot/output/NC20C_RMfRST_100_rootcandidates.json \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--scores ../rdaroot/output/NC20C_RMfRST_100_rootscores.csv \
--no-debug


# Generate & score 1,000-plan ensembles

scripts/rmfrst_ensemble.py \
--state NC \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--size 1000 \
--plans output/NC20C_RMfRST_1000_plans.json \
--log output/NC20C_RMfRST_1000_log.txt \
--no-debug

scripts/score_ensemble.py \
--state NC \
--plans output/NC20C_RMfRST_1000_plans.json \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--scores output/NC20C_RMfRST_1000_scores.csv \
--no-debug