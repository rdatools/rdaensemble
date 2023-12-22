# Generate & score 100-plan ensemble from random spanning trees

scripts/rmfrst_ensemble.py \
--state NC \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--size 100 \
--plans ensembles/NC20C_RMfRST_100_plans.json \
--log ensembles/NC20C_RMfRST_100_log.txt \
--no-debug

scripts/score_ensemble.py \
--state NC \
--plans ensembles/NC20C_RMfRST_100_plans.json \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--scores ensembles/NC20C_RMfRST_100_scores.csv \
--no-debug

# Generate 100-plan ensemble from random starting points

scripts/rmfrsp_ensemble.py \
--state NC \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--size 100 \
--plans ensembles/NC20C_RMfRSP_100_plans.json \
--log ensembles/NC20C_RMfRSP_100_log.txt \
--no-debug

# Score root map candidates

scripts/score_ensemble.py \
--state NC \
--plans ../rdaroot/ensembles/NC20C_RMfRST_100_rootcandidates.json \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--scores ../rdaroot/ensembles/NC20C_RMfRST_100_rootscores.csv \
--no-debug


# Generate & score 1,000-plan ensemble from random spanning trees

scripts/rmfrst_ensemble.py \
--state NC \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--size 1000 \
--plans ensembles/NC20C_RMfRST_1000_plans.json \
--log ensembles/NC20C_RMfRST_1000_log.txt \
--no-debug

scripts/score_ensemble.py \
--state NC \
--plans ensembles/NC20C_RMfRST_1000_plans.json \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--scores ensembles/NC20C_RMfRST_1000_scores.csv \
--no-debug

scripts/id_notable_maps.py \
--scores ensembles/NC20C_RMfRST_1000_scores.csv \
--metadata ensembles/NC20C_RMfRST_1000_scores_metadata.json \
--notables ensembles/NC20C_RMfRST_1000_notables_maps.json \
--splitting 0 \
--no-debug

# Generate & score 1,000-plan ReCom ensemble

scripts/recom_ensemble.py \
--state NC \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--size 1000 \
--plans ensembles/NC20C_ReCom_1000_plans.json \
--log ensembles/NC20C_ReCom_1000_log.txt \
--no-debug

scripts/score_ensemble.py \
--state NC \
--plans ensembles/NC20C_ReCom_1000_plans.json \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--scores ensembles/NC20C_ReCom_1000_scores.csv \
--no-debug

scripts/id_notable_maps.py \
--scores ensembles/NC20C_ReCom_1000_scores.csv \
--metadata ensembles/NC20C_ReCom_1000_scores_metadata.json \
--notables ensembles/NC20C_ReCom_1000_notables_maps.json \
--splitting 0 \
--no-debug