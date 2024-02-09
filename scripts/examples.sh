# Generate & score 100-plan ensemble from random spanning trees

scripts/rmfrst_ensemble.py \
--state NC \
--size 100 \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--plans ../../iCloud/fileout/ensembles/NC20C_RMfRST_100_plans.json \
--log ../../iCloud/fileout/ensembles/NC20C_RMfRST_100_log.txt \
--no-debug

scripts/score_ensemble.py \
--state NC \
--plans ../../iCloud/fileout/ensembles/NC20C_RMfRST_100_plans.json \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--scores ../../iCloud/fileout/ensembles/NC20C_RMfRST_100_scores.csv \
--no-debug

# Generate 100-plan ensemble from random starting points

scripts/rmfrsp_ensemble.py \
--state NC \
--size 100 \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--plans ../../iCloud/fileout/ensembles/NC20C_RMfRSP_100_plans.json \
--log ../../iCloud/fileout/ensembles/NC20C_RMfRSP_100_log.txt \
--no-debug

# Score root map candidates

scripts/score_ensemble.py \
--state NC \
--plans ../rdaroot/../../iCloud/fileout/ensembles/NC20C_RMfRST_100_rootcandidates.json \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--scores ../rdaroot/../../iCloud/fileout/ensembles/NC20C_RMfRST_100_rootscores.csv \
--no-debug


# Generate & score 1,000-plan ensemble from random spanning trees

scripts/rmfrst_ensemble.py \
--state NC \
--size 1000 \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--plans ../../iCloud/fileout/ensembles/NC20C_RMfRST_1K_plans.json \
--log ../../iCloud/fileout/ensembles/NC20C_RMfRST_1K_log.txt \
--no-debug

scripts/score_ensemble.py \
--state NC \
--plans ../../iCloud/fileout/ensembles/NC20C_RMfRST_1K_plans.json \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--scores ../../iCloud/fileout/ensembles/NC20C_RMfRST_1K_scores.csv \
--no-debug

scripts/id_notable_maps.py \
--scores ../../iCloud/fileout/ensembles/NC20C_RMfRST_1K_scores.csv \
--metadata ../../iCloud/fileout/ensembles/NC20C_RMfRST_1K_scores_metadata.json \
--notables ../../iCloud/fileout/ensembles/NC20C_RMfRST_1K_notables_maps.json \
--splitting 0 \
--no-debug

# Generate & score 1,000-plan ReCom ensemble

scripts/recom_ensemble.py \
--state NC \
--size 1000 \
--data ../rdabase/data/NC/NC_2020_data.csv \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--root ../rdaroot/../../iCloud/fileout/ensembles/NC20C_RMfRST_100_root_map.csv \
--plans ../../iCloud/fileout/ensembles/NC20C_ReCom_1K_plans.json \
--log ../../iCloud/fileout/ensembles/NC20C_ReCom_1K_log.txt \
--no-debug

scripts/score_ensemble.py \
--state NC \
--plans ../../iCloud/fileout/ensembles/NC20C_ReCom_1K_plans.json \
--data ../rdabase/data/NC/NC_2020_data.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--scores ../../iCloud/fileout/ensembles/NC20C_ReCom_1K_scores.csv \
--no-debug

scripts/id_notable_maps.py \
--scores ../../iCloud/fileout/ensembles/NC20C_ReCom_1K_scores.csv \
--metadata ../../iCloud/fileout/ensembles/NC20C_ReCom_1K_scores_metadata.json \
--notables ../../iCloud/fileout/ensembles/NC20C_ReCom_1K_notables_maps.json \
--splitting 0 \
--no-debug