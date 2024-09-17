echo 'Running AL congress 7 ...'
scripts/random_map.py --state AL --plantype congress --roughlyequal 0.01 --data ../rdabase/data/AL/AL_2020_data.csv --shapes ../rdabase/data/AL/AL_2020_shapes_simplified.json --graph ../rdabase/data/AL/AL_2020_graph.json --output temp/AL20C_random_plan.csv --log temp/AL20C_random_log.txt --no-debug
echo 'Running AL upper 35 ...'
scripts/random_map.py --state AL --plantype upper --roughlyequal 0.1 --data ../rdabase/data/AL/AL_2020_data.csv --shapes ../rdabase/data/AL/AL_2020_shapes_simplified.json --graph ../rdabase/data/AL/AL_2020_graph.json --output temp/AL20U_random_plan.csv --log temp/AL20U_random_log.txt --no-debug
echo 'Running AL lower 105 ...'
scripts/random_map.py --state AL --plantype lower --roughlyequal 0.1 --data ../rdabase/data/AL/AL_2020_data.csv --shapes ../rdabase/data/AL/AL_2020_shapes_simplified.json --graph ../rdabase/data/AL/AL_2020_graph.json --output temp/AL20L_random_plan.csv --log temp/AL20L_random_log.txt --no-debug
echo 'Running AK upper 20 ...'
# scripts/random_map.py --state AK --plantype upper --roughlyequal 0.1 --data ../rdabase/data/AK/AK_2020_data.csv --shapes ../rdabase/data/AK/AK_2020_shapes_simplified.json --graph ../rdabase/data/AK/AK_2020_graph.json --output temp/AK20U_random_plan.csv --log temp/AK20U_random_log.txt --no-debug
echo 'Running AK lower 40 ...'
# scripts/random_map.py --state AK --plantype lower --roughlyequal 0.1 --data ../rdabase/data/AK/AK_2020_data.csv --shapes ../rdabase/data/AK/AK_2020_shapes_simplified.json --graph ../rdabase/data/AK/AK_2020_graph.json --output temp/AK20L_random_plan.csv --log temp/AK20L_random_log.txt --no-debug
echo 'Running AZ congress 9 ...'
scripts/random_map.py --state AZ --plantype congress --roughlyequal 0.01 --data ../rdabase/data/AZ/AZ_2020_data.csv --shapes ../rdabase/data/AZ/AZ_2020_shapes_simplified.json --graph ../rdabase/data/AZ/AZ_2020_graph.json --output temp/AZ20C_random_plan.csv --log temp/AZ20C_random_log.txt --no-debug
echo 'Running AZ upper 30 ...'
scripts/random_map.py --state AZ --plantype upper --roughlyequal 0.1 --data ../rdabase/data/AZ/AZ_2020_data.csv --shapes ../rdabase/data/AZ/AZ_2020_shapes_simplified.json --graph ../rdabase/data/AZ/AZ_2020_graph.json --output temp/AZ20U_random_plan.csv --log temp/AZ20U_random_log.txt --no-debug
echo 'Running AR congress 4 ...'
# scripts/random_map.py --state AR --plantype congress --roughlyequal 0.01 --data ../rdabase/data/AR/AR_2020_data.csv --shapes ../rdabase/data/AR/AR_2020_shapes_simplified.json --graph ../rdabase/data/AR/AR_2020_graph.json --output temp/AR20C_random_plan.csv --log temp/AR20C_random_log.txt --no-debug
echo 'Running AR upper 35 ...'
# scripts/random_map.py --state AR --plantype upper --roughlyequal 0.1 --data ../rdabase/data/AR/AR_2020_data.csv --shapes ../rdabase/data/AR/AR_2020_shapes_simplified.json --graph ../rdabase/data/AR/AR_2020_graph.json --output temp/AR20U_random_plan.csv --log temp/AR20U_random_log.txt --no-debug
echo 'Running AR lower 100 ...'
# scripts/random_map.py --state AR --plantype lower --roughlyequal 0.1 --data ../rdabase/data/AR/AR_2020_data.csv --shapes ../rdabase/data/AR/AR_2020_shapes_simplified.json --graph ../rdabase/data/AR/AR_2020_graph.json --output temp/AR20L_random_plan.csv --log temp/AR20L_random_log.txt --no-debug
echo 'Running CA congress 52 ...'
# scripts/random_map.py --state CA --plantype congress --roughlyequal 0.01 --data ../rdabase/data/CA/CA_2020_data.csv --shapes ../rdabase/data/CA/CA_2020_shapes_simplified.json --graph ../rdabase/data/CA/CA_2020_graph.json --output temp/CA20C_random_plan.csv --log temp/CA20C_random_log.txt --no-debug
echo 'Running CA upper 40 ...'
# scripts/random_map.py --state CA --plantype upper --roughlyequal 0.1 --data ../rdabase/data/CA/CA_2020_data.csv --shapes ../rdabase/data/CA/CA_2020_shapes_simplified.json --graph ../rdabase/data/CA/CA_2020_graph.json --output temp/CA20U_random_plan.csv --log temp/CA20U_random_log.txt --no-debug
echo 'Running CA lower 80 ...'
# scripts/random_map.py --state CA --plantype lower --roughlyequal 0.1 --data ../rdabase/data/CA/CA_2020_data.csv --shapes ../rdabase/data/CA/CA_2020_shapes_simplified.json --graph ../rdabase/data/CA/CA_2020_graph.json --output temp/CA20L_random_plan.csv --log temp/CA20L_random_log.txt --no-debug
echo 'Running CO congress 8 ...'
# scripts/random_map.py --state CO --plantype congress --roughlyequal 0.01 --data ../rdabase/data/CO/CO_2020_data.csv --shapes ../rdabase/data/CO/CO_2020_shapes_simplified.json --graph ../rdabase/data/CO/CO_2020_graph.json --output temp/CO20C_random_plan.csv --log temp/CO20C_random_log.txt --no-debug
echo 'Running CO upper 35 ...'
# scripts/random_map.py --state CO --plantype upper --roughlyequal 0.1 --data ../rdabase/data/CO/CO_2020_data.csv --shapes ../rdabase/data/CO/CO_2020_shapes_simplified.json --graph ../rdabase/data/CO/CO_2020_graph.json --output temp/CO20U_random_plan.csv --log temp/CO20U_random_log.txt --no-debug
echo 'Running CO lower 65 ...'
# scripts/random_map.py --state CO --plantype lower --roughlyequal 0.1 --data ../rdabase/data/CO/CO_2020_data.csv --shapes ../rdabase/data/CO/CO_2020_shapes_simplified.json --graph ../rdabase/data/CO/CO_2020_graph.json --output temp/CO20L_random_plan.csv --log temp/CO20L_random_log.txt --no-debug
echo 'Running CT congress 5 ...'
# scripts/random_map.py --state CT --plantype congress --roughlyequal 0.01 --data ../rdabase/data/CT/CT_2020_data.csv --shapes ../rdabase/data/CT/CT_2020_shapes_simplified.json --graph ../rdabase/data/CT/CT_2020_graph.json --output temp/CT20C_random_plan.csv --log temp/CT20C_random_log.txt --no-debug
echo 'Running CT upper 36 ...'
# scripts/random_map.py --state CT --plantype upper --roughlyequal 0.1 --data ../rdabase/data/CT/CT_2020_data.csv --shapes ../rdabase/data/CT/CT_2020_shapes_simplified.json --graph ../rdabase/data/CT/CT_2020_graph.json --output temp/CT20U_random_plan.csv --log temp/CT20U_random_log.txt --no-debug
echo 'Running CT lower 151 ...'
# scripts/random_map.py --state CT --plantype lower --roughlyequal 0.1 --data ../rdabase/data/CT/CT_2020_data.csv --shapes ../rdabase/data/CT/CT_2020_shapes_simplified.json --graph ../rdabase/data/CT/CT_2020_graph.json --output temp/CT20L_random_plan.csv --log temp/CT20L_random_log.txt --no-debug
echo 'Running DE upper 21 ...'
# scripts/random_map.py --state DE --plantype upper --roughlyequal 0.1 --data ../rdabase/data/DE/DE_2020_data.csv --shapes ../rdabase/data/DE/DE_2020_shapes_simplified.json --graph ../rdabase/data/DE/DE_2020_graph.json --output temp/DE20U_random_plan.csv --log temp/DE20U_random_log.txt --no-debug
echo 'Running DE lower 41 ...'
# scripts/random_map.py --state DE --plantype lower --roughlyequal 0.1 --data ../rdabase/data/DE/DE_2020_data.csv --shapes ../rdabase/data/DE/DE_2020_shapes_simplified.json --graph ../rdabase/data/DE/DE_2020_graph.json --output temp/DE20L_random_plan.csv --log temp/DE20L_random_log.txt --no-debug
echo 'Running FL congress 28 ...'
scripts/random_map.py --state FL --plantype congress --roughlyequal 0.01 --data ../rdabase/data/FL/FL_2020_data.csv --shapes ../rdabase/data/FL/FL_2020_shapes_simplified.json --graph ../rdabase/data/FL/FL_2020_graph.json --output temp/FL20C_random_plan.csv --log temp/FL20C_random_log.txt --no-debug
echo 'Running FL upper 40 ...'
scripts/random_map.py --state FL --plantype upper --roughlyequal 0.1 --data ../rdabase/data/FL/FL_2020_data.csv --shapes ../rdabase/data/FL/FL_2020_shapes_simplified.json --graph ../rdabase/data/FL/FL_2020_graph.json --output temp/FL20U_random_plan.csv --log temp/FL20U_random_log.txt --no-debug
echo 'Running FL lower 120 ...'
scripts/random_map.py --state FL --plantype lower --roughlyequal 0.1 --data ../rdabase/data/FL/FL_2020_data.csv --shapes ../rdabase/data/FL/FL_2020_shapes_simplified.json --graph ../rdabase/data/FL/FL_2020_graph.json --output temp/FL20L_random_plan.csv --log temp/FL20L_random_log.txt --no-debug
echo 'Running GA congress 14 ...'
scripts/random_map.py --state GA --plantype congress --roughlyequal 0.01 --data ../rdabase/data/GA/GA_2020_data.csv --shapes ../rdabase/data/GA/GA_2020_shapes_simplified.json --graph ../rdabase/data/GA/GA_2020_graph.json --output temp/GA20C_random_plan.csv --log temp/GA20C_random_log.txt --no-debug
echo 'Running GA upper 56 ...'
scripts/random_map.py --state GA --plantype upper --roughlyequal 0.1 --data ../rdabase/data/GA/GA_2020_data.csv --shapes ../rdabase/data/GA/GA_2020_shapes_simplified.json --graph ../rdabase/data/GA/GA_2020_graph.json --output temp/GA20U_random_plan.csv --log temp/GA20U_random_log.txt --no-debug
echo 'Running GA lower 180 ...'
scripts/random_map.py --state GA --plantype lower --roughlyequal 0.1 --data ../rdabase/data/GA/GA_2020_data.csv --shapes ../rdabase/data/GA/GA_2020_shapes_simplified.json --graph ../rdabase/data/GA/GA_2020_graph.json --output temp/GA20L_random_plan.csv --log temp/GA20L_random_log.txt --no-debug
echo 'Running HI congress 2 ...'
# scripts/random_map.py --state HI --plantype congress --roughlyequal 0.01 --data ../rdabase/data/HI/HI_2020_data.csv --shapes ../rdabase/data/HI/HI_2020_shapes_simplified.json --graph ../rdabase/data/HI/HI_2020_graph.json --output temp/HI20C_random_plan.csv --log temp/HI20C_random_log.txt --no-debug
echo 'Running HI upper 25 ...'
# scripts/random_map.py --state HI --plantype upper --roughlyequal 0.1 --data ../rdabase/data/HI/HI_2020_data.csv --shapes ../rdabase/data/HI/HI_2020_shapes_simplified.json --graph ../rdabase/data/HI/HI_2020_graph.json --output temp/HI20U_random_plan.csv --log temp/HI20U_random_log.txt --no-debug
echo 'Running HI lower 51 ...'
# scripts/random_map.py --state HI --plantype lower --roughlyequal 0.1 --data ../rdabase/data/HI/HI_2020_data.csv --shapes ../rdabase/data/HI/HI_2020_shapes_simplified.json --graph ../rdabase/data/HI/HI_2020_graph.json --output temp/HI20L_random_plan.csv --log temp/HI20L_random_log.txt --no-debug
echo 'Running ID congress 2 ...'
# scripts/random_map.py --state ID --plantype congress --roughlyequal 0.01 --data ../rdabase/data/ID/ID_2020_data.csv --shapes ../rdabase/data/ID/ID_2020_shapes_simplified.json --graph ../rdabase/data/ID/ID_2020_graph.json --output temp/ID20C_random_plan.csv --log temp/ID20C_random_log.txt --no-debug
echo 'Running ID upper 35 ...'
# scripts/random_map.py --state ID --plantype upper --roughlyequal 0.1 --data ../rdabase/data/ID/ID_2020_data.csv --shapes ../rdabase/data/ID/ID_2020_shapes_simplified.json --graph ../rdabase/data/ID/ID_2020_graph.json --output temp/ID20U_random_plan.csv --log temp/ID20U_random_log.txt --no-debug
echo 'Running IL congress 17 ...'
scripts/random_map.py --state IL --plantype congress --roughlyequal 0.01 --data ../rdabase/data/IL/IL_2020_data.csv --shapes ../rdabase/data/IL/IL_2020_shapes_simplified.json --graph ../rdabase/data/IL/IL_2020_graph.json --output temp/IL20C_random_plan.csv --log temp/IL20C_random_log.txt --no-debug
echo 'Running IL upper 59 ...'
scripts/random_map.py --state IL --plantype upper --roughlyequal 0.1 --data ../rdabase/data/IL/IL_2020_data.csv --shapes ../rdabase/data/IL/IL_2020_shapes_simplified.json --graph ../rdabase/data/IL/IL_2020_graph.json --output temp/IL20U_random_plan.csv --log temp/IL20U_random_log.txt --no-debug
echo 'Running IL lower 118 ...'
scripts/random_map.py --state IL --plantype lower --roughlyequal 0.1 --data ../rdabase/data/IL/IL_2020_data.csv --shapes ../rdabase/data/IL/IL_2020_shapes_simplified.json --graph ../rdabase/data/IL/IL_2020_graph.json --output temp/IL20L_random_plan.csv --log temp/IL20L_random_log.txt --no-debug
echo 'Running IN congress 9 ...'
scripts/random_map.py --state IN --plantype congress --roughlyequal 0.01 --data ../rdabase/data/IN/IN_2020_data.csv --shapes ../rdabase/data/IN/IN_2020_shapes_simplified.json --graph ../rdabase/data/IN/IN_2020_graph.json --output temp/IN20C_random_plan.csv --log temp/IN20C_random_log.txt --no-debug
echo 'Running IN upper 50 ...'
scripts/random_map.py --state IN --plantype upper --roughlyequal 0.1 --data ../rdabase/data/IN/IN_2020_data.csv --shapes ../rdabase/data/IN/IN_2020_shapes_simplified.json --graph ../rdabase/data/IN/IN_2020_graph.json --output temp/IN20U_random_plan.csv --log temp/IN20U_random_log.txt --no-debug
echo 'Running IN lower 100 ...'
scripts/random_map.py --state IN --plantype lower --roughlyequal 0.1 --data ../rdabase/data/IN/IN_2020_data.csv --shapes ../rdabase/data/IN/IN_2020_shapes_simplified.json --graph ../rdabase/data/IN/IN_2020_graph.json --output temp/IN20L_random_plan.csv --log temp/IN20L_random_log.txt --no-debug
echo 'Running IA congress 4 ...'
# scripts/random_map.py --state IA --plantype congress --roughlyequal 0.01 --data ../rdabase/data/IA/IA_2020_data.csv --shapes ../rdabase/data/IA/IA_2020_shapes_simplified.json --graph ../rdabase/data/IA/IA_2020_graph.json --output temp/IA20C_random_plan.csv --log temp/IA20C_random_log.txt --no-debug
echo 'Running IA upper 50 ...'
# scripts/random_map.py --state IA --plantype upper --roughlyequal 0.1 --data ../rdabase/data/IA/IA_2020_data.csv --shapes ../rdabase/data/IA/IA_2020_shapes_simplified.json --graph ../rdabase/data/IA/IA_2020_graph.json --output temp/IA20U_random_plan.csv --log temp/IA20U_random_log.txt --no-debug
echo 'Running IA lower 100 ...'
# scripts/random_map.py --state IA --plantype lower --roughlyequal 0.1 --data ../rdabase/data/IA/IA_2020_data.csv --shapes ../rdabase/data/IA/IA_2020_shapes_simplified.json --graph ../rdabase/data/IA/IA_2020_graph.json --output temp/IA20L_random_plan.csv --log temp/IA20L_random_log.txt --no-debug
echo 'Running KS congress 4 ...'
# scripts/random_map.py --state KS --plantype congress --roughlyequal 0.01 --data ../rdabase/data/KS/KS_2020_data.csv --shapes ../rdabase/data/KS/KS_2020_shapes_simplified.json --graph ../rdabase/data/KS/KS_2020_graph.json --output temp/KS20C_random_plan.csv --log temp/KS20C_random_log.txt --no-debug
echo 'Running KS upper 40 ...'
# scripts/random_map.py --state KS --plantype upper --roughlyequal 0.1 --data ../rdabase/data/KS/KS_2020_data.csv --shapes ../rdabase/data/KS/KS_2020_shapes_simplified.json --graph ../rdabase/data/KS/KS_2020_graph.json --output temp/KS20U_random_plan.csv --log temp/KS20U_random_log.txt --no-debug
echo 'Running KS lower 125 ...'
# scripts/random_map.py --state KS --plantype lower --roughlyequal 0.1 --data ../rdabase/data/KS/KS_2020_data.csv --shapes ../rdabase/data/KS/KS_2020_shapes_simplified.json --graph ../rdabase/data/KS/KS_2020_graph.json --output temp/KS20L_random_plan.csv --log temp/KS20L_random_log.txt --no-debug
echo 'Running KY congress 6 ...'
# scripts/random_map.py --state KY --plantype congress --roughlyequal 0.01 --data ../rdabase/data/KY/KY_2020_data.csv --shapes ../rdabase/data/KY/KY_2020_shapes_simplified.json --graph ../rdabase/data/KY/KY_2020_graph.json --output temp/KY20C_random_plan.csv --log temp/KY20C_random_log.txt --no-debug
echo 'Running KY upper 38 ...'
# scripts/random_map.py --state KY --plantype upper --roughlyequal 0.1 --data ../rdabase/data/KY/KY_2020_data.csv --shapes ../rdabase/data/KY/KY_2020_shapes_simplified.json --graph ../rdabase/data/KY/KY_2020_graph.json --output temp/KY20U_random_plan.csv --log temp/KY20U_random_log.txt --no-debug
echo 'Running KY lower 100 ...'
# scripts/random_map.py --state KY --plantype lower --roughlyequal 0.1 --data ../rdabase/data/KY/KY_2020_data.csv --shapes ../rdabase/data/KY/KY_2020_shapes_simplified.json --graph ../rdabase/data/KY/KY_2020_graph.json --output temp/KY20L_random_plan.csv --log temp/KY20L_random_log.txt --no-debug
echo 'Running LA congress 6 ...'
# scripts/random_map.py --state LA --plantype congress --roughlyequal 0.01 --data ../rdabase/data/LA/LA_2020_data.csv --shapes ../rdabase/data/LA/LA_2020_shapes_simplified.json --graph ../rdabase/data/LA/LA_2020_graph.json --output temp/LA20C_random_plan.csv --log temp/LA20C_random_log.txt --no-debug
echo 'Running LA upper 39 ...'
# scripts/random_map.py --state LA --plantype upper --roughlyequal 0.1 --data ../rdabase/data/LA/LA_2020_data.csv --shapes ../rdabase/data/LA/LA_2020_shapes_simplified.json --graph ../rdabase/data/LA/LA_2020_graph.json --output temp/LA20U_random_plan.csv --log temp/LA20U_random_log.txt --no-debug
echo 'Running LA lower 105 ...'
# scripts/random_map.py --state LA --plantype lower --roughlyequal 0.1 --data ../rdabase/data/LA/LA_2020_data.csv --shapes ../rdabase/data/LA/LA_2020_shapes_simplified.json --graph ../rdabase/data/LA/LA_2020_graph.json --output temp/LA20L_random_plan.csv --log temp/LA20L_random_log.txt --no-debug
echo 'Running ME congress 2 ...'
# scripts/random_map.py --state ME --plantype congress --roughlyequal 0.01 --data ../rdabase/data/ME/ME_2020_data.csv --shapes ../rdabase/data/ME/ME_2020_shapes_simplified.json --graph ../rdabase/data/ME/ME_2020_graph.json --output temp/ME20C_random_plan.csv --log temp/ME20C_random_log.txt --no-debug
echo 'Running ME upper 35 ...'
# scripts/random_map.py --state ME --plantype upper --roughlyequal 0.1 --data ../rdabase/data/ME/ME_2020_data.csv --shapes ../rdabase/data/ME/ME_2020_shapes_simplified.json --graph ../rdabase/data/ME/ME_2020_graph.json --output temp/ME20U_random_plan.csv --log temp/ME20U_random_log.txt --no-debug
echo 'Running ME lower 151 ...'
# scripts/random_map.py --state ME --plantype lower --roughlyequal 0.1 --data ../rdabase/data/ME/ME_2020_data.csv --shapes ../rdabase/data/ME/ME_2020_shapes_simplified.json --graph ../rdabase/data/ME/ME_2020_graph.json --output temp/ME20L_random_plan.csv --log temp/ME20L_random_log.txt --no-debug
echo 'Running MD congress 8 ...'
scripts/random_map.py --state MD --plantype congress --roughlyequal 0.01 --data ../rdabase/data/MD/MD_2020_data.csv --shapes ../rdabase/data/MD/MD_2020_shapes_simplified.json --graph ../rdabase/data/MD/MD_2020_graph.json --output temp/MD20C_random_plan.csv --log temp/MD20C_random_log.txt --no-debug
echo 'Running MD upper 47 ...'
scripts/random_map.py --state MD --plantype upper --roughlyequal 0.1 --data ../rdabase/data/MD/MD_2020_data.csv --shapes ../rdabase/data/MD/MD_2020_shapes_simplified.json --graph ../rdabase/data/MD/MD_2020_graph.json --output temp/MD20U_random_plan.csv --log temp/MD20U_random_log.txt --no-debug
echo 'Running MA congress 9 ...'
# scripts/random_map.py --state MA --plantype congress --roughlyequal 0.01 --data ../rdabase/data/MA/MA_2020_data.csv --shapes ../rdabase/data/MA/MA_2020_shapes_simplified.json --graph ../rdabase/data/MA/MA_2020_graph.json --output temp/MA20C_random_plan.csv --log temp/MA20C_random_log.txt --no-debug
echo 'Running MA upper 40 ...'
# scripts/random_map.py --state MA --plantype upper --roughlyequal 0.1 --data ../rdabase/data/MA/MA_2020_data.csv --shapes ../rdabase/data/MA/MA_2020_shapes_simplified.json --graph ../rdabase/data/MA/MA_2020_graph.json --output temp/MA20U_random_plan.csv --log temp/MA20U_random_log.txt --no-debug
echo 'Running MA lower 160 ...'
# scripts/random_map.py --state MA --plantype lower --roughlyequal 0.1 --data ../rdabase/data/MA/MA_2020_data.csv --shapes ../rdabase/data/MA/MA_2020_shapes_simplified.json --graph ../rdabase/data/MA/MA_2020_graph.json --output temp/MA20L_random_plan.csv --log temp/MA20L_random_log.txt --no-debug
echo 'Running MI congress 13 ...'
scripts/random_map.py --state MI --plantype congress --roughlyequal 0.01 --data ../rdabase/data/MI/MI_2020_data.csv --shapes ../rdabase/data/MI/MI_2020_shapes_simplified.json --graph ../rdabase/data/MI/MI_2020_graph.json --output temp/MI20C_random_plan.csv --log temp/MI20C_random_log.txt --no-debug
echo 'Running MI upper 38 ...'
scripts/random_map.py --state MI --plantype upper --roughlyequal 0.1 --data ../rdabase/data/MI/MI_2020_data.csv --shapes ../rdabase/data/MI/MI_2020_shapes_simplified.json --graph ../rdabase/data/MI/MI_2020_graph.json --output temp/MI20U_random_plan.csv --log temp/MI20U_random_log.txt --no-debug
echo 'Running MI lower 110 ...'
scripts/random_map.py --state MI --plantype lower --roughlyequal 0.1 --data ../rdabase/data/MI/MI_2020_data.csv --shapes ../rdabase/data/MI/MI_2020_shapes_simplified.json --graph ../rdabase/data/MI/MI_2020_graph.json --output temp/MI20L_random_plan.csv --log temp/MI20L_random_log.txt --no-debug
echo 'Running MN congress 8 ...'
# scripts/random_map.py --state MN --plantype congress --roughlyequal 0.01 --data ../rdabase/data/MN/MN_2020_data.csv --shapes ../rdabase/data/MN/MN_2020_shapes_simplified.json --graph ../rdabase/data/MN/MN_2020_graph.json --output temp/MN20C_random_plan.csv --log temp/MN20C_random_log.txt --no-debug
echo 'Running MN upper 67 ...'
# scripts/random_map.py --state MN --plantype upper --roughlyequal 0.1 --data ../rdabase/data/MN/MN_2020_data.csv --shapes ../rdabase/data/MN/MN_2020_shapes_simplified.json --graph ../rdabase/data/MN/MN_2020_graph.json --output temp/MN20U_random_plan.csv --log temp/MN20U_random_log.txt --no-debug
echo 'Running MN lower 134 ...'
# scripts/random_map.py --state MN --plantype lower --roughlyequal 0.1 --data ../rdabase/data/MN/MN_2020_data.csv --shapes ../rdabase/data/MN/MN_2020_shapes_simplified.json --graph ../rdabase/data/MN/MN_2020_graph.json --output temp/MN20L_random_plan.csv --log temp/MN20L_random_log.txt --no-debug
echo 'Running MS congress 4 ...'
# scripts/random_map.py --state MS --plantype congress --roughlyequal 0.01 --data ../rdabase/data/MS/MS_2020_data.csv --shapes ../rdabase/data/MS/MS_2020_shapes_simplified.json --graph ../rdabase/data/MS/MS_2020_graph.json --output temp/MS20C_random_plan.csv --log temp/MS20C_random_log.txt --no-debug
echo 'Running MS upper 52 ...'
# scripts/random_map.py --state MS --plantype upper --roughlyequal 0.1 --data ../rdabase/data/MS/MS_2020_data.csv --shapes ../rdabase/data/MS/MS_2020_shapes_simplified.json --graph ../rdabase/data/MS/MS_2020_graph.json --output temp/MS20U_random_plan.csv --log temp/MS20U_random_log.txt --no-debug
echo 'Running MS lower 122 ...'
# scripts/random_map.py --state MS --plantype lower --roughlyequal 0.1 --data ../rdabase/data/MS/MS_2020_data.csv --shapes ../rdabase/data/MS/MS_2020_shapes_simplified.json --graph ../rdabase/data/MS/MS_2020_graph.json --output temp/MS20L_random_plan.csv --log temp/MS20L_random_log.txt --no-debug
echo 'Running MO congress 8 ...'
# scripts/random_map.py --state MO --plantype congress --roughlyequal 0.01 --data ../rdabase/data/MO/MO_2020_data.csv --shapes ../rdabase/data/MO/MO_2020_shapes_simplified.json --graph ../rdabase/data/MO/MO_2020_graph.json --output temp/MO20C_random_plan.csv --log temp/MO20C_random_log.txt --no-debug
echo 'Running MO upper 34 ...'
# scripts/random_map.py --state MO --plantype upper --roughlyequal 0.1 --data ../rdabase/data/MO/MO_2020_data.csv --shapes ../rdabase/data/MO/MO_2020_shapes_simplified.json --graph ../rdabase/data/MO/MO_2020_graph.json --output temp/MO20U_random_plan.csv --log temp/MO20U_random_log.txt --no-debug
echo 'Running MO lower 163 ...'
# scripts/random_map.py --state MO --plantype lower --roughlyequal 0.1 --data ../rdabase/data/MO/MO_2020_data.csv --shapes ../rdabase/data/MO/MO_2020_shapes_simplified.json --graph ../rdabase/data/MO/MO_2020_graph.json --output temp/MO20L_random_plan.csv --log temp/MO20L_random_log.txt --no-debug
echo 'Running MT congress 2 ...'
# scripts/random_map.py --state MT --plantype congress --roughlyequal 0.01 --data ../rdabase/data/MT/MT_2020_data.csv --shapes ../rdabase/data/MT/MT_2020_shapes_simplified.json --graph ../rdabase/data/MT/MT_2020_graph.json --output temp/MT20C_random_plan.csv --log temp/MT20C_random_log.txt --no-debug
echo 'Running MT upper 50 ...'
# scripts/random_map.py --state MT --plantype upper --roughlyequal 0.1 --data ../rdabase/data/MT/MT_2020_data.csv --shapes ../rdabase/data/MT/MT_2020_shapes_simplified.json --graph ../rdabase/data/MT/MT_2020_graph.json --output temp/MT20U_random_plan.csv --log temp/MT20U_random_log.txt --no-debug
echo 'Running MT lower 100 ...'
# scripts/random_map.py --state MT --plantype lower --roughlyequal 0.1 --data ../rdabase/data/MT/MT_2020_data.csv --shapes ../rdabase/data/MT/MT_2020_shapes_simplified.json --graph ../rdabase/data/MT/MT_2020_graph.json --output temp/MT20L_random_plan.csv --log temp/MT20L_random_log.txt --no-debug
echo 'Running NE congress 3 ...'
# scripts/random_map.py --state NE --plantype congress --roughlyequal 0.01 --data ../rdabase/data/NE/NE_2020_data.csv --shapes ../rdabase/data/NE/NE_2020_shapes_simplified.json --graph ../rdabase/data/NE/NE_2020_graph.json --output temp/NE20C_random_plan.csv --log temp/NE20C_random_log.txt --no-debug
echo 'Running NE upper 49 ...'
# scripts/random_map.py --state NE --plantype upper --roughlyequal 0.1 --data ../rdabase/data/NE/NE_2020_data.csv --shapes ../rdabase/data/NE/NE_2020_shapes_simplified.json --graph ../rdabase/data/NE/NE_2020_graph.json --output temp/NE20U_random_plan.csv --log temp/NE20U_random_log.txt --no-debug
echo 'Running NV congress 4 ...'
# scripts/random_map.py --state NV --plantype congress --roughlyequal 0.01 --data ../rdabase/data/NV/NV_2020_data.csv --shapes ../rdabase/data/NV/NV_2020_shapes_simplified.json --graph ../rdabase/data/NV/NV_2020_graph.json --output temp/NV20C_random_plan.csv --log temp/NV20C_random_log.txt --no-debug
echo 'Running NV upper 21 ...'
# scripts/random_map.py --state NV --plantype upper --roughlyequal 0.1 --data ../rdabase/data/NV/NV_2020_data.csv --shapes ../rdabase/data/NV/NV_2020_shapes_simplified.json --graph ../rdabase/data/NV/NV_2020_graph.json --output temp/NV20U_random_plan.csv --log temp/NV20U_random_log.txt --no-debug
echo 'Running NV lower 42 ...'
# scripts/random_map.py --state NV --plantype lower --roughlyequal 0.1 --data ../rdabase/data/NV/NV_2020_data.csv --shapes ../rdabase/data/NV/NV_2020_shapes_simplified.json --graph ../rdabase/data/NV/NV_2020_graph.json --output temp/NV20L_random_plan.csv --log temp/NV20L_random_log.txt --no-debug
echo 'Running NH congress 2 ...'
# scripts/random_map.py --state NH --plantype congress --roughlyequal 0.01 --data ../rdabase/data/NH/NH_2020_data.csv --shapes ../rdabase/data/NH/NH_2020_shapes_simplified.json --graph ../rdabase/data/NH/NH_2020_graph.json --output temp/NH20C_random_plan.csv --log temp/NH20C_random_log.txt --no-debug
echo 'Running NH upper 24 ...'
# scripts/random_map.py --state NH --plantype upper --roughlyequal 0.1 --data ../rdabase/data/NH/NH_2020_data.csv --shapes ../rdabase/data/NH/NH_2020_shapes_simplified.json --graph ../rdabase/data/NH/NH_2020_graph.json --output temp/NH20U_random_plan.csv --log temp/NH20U_random_log.txt --no-debug
echo 'Running NH lower 164 ...'
# scripts/random_map.py --state NH --plantype lower --roughlyequal 0.1 --data ../rdabase/data/NH/NH_2020_data.csv --shapes ../rdabase/data/NH/NH_2020_shapes_simplified.json --graph ../rdabase/data/NH/NH_2020_graph.json --output temp/NH20L_random_plan.csv --log temp/NH20L_random_log.txt --no-debug
echo 'Running NJ congress 12 ...'
scripts/random_map.py --state NJ --plantype congress --roughlyequal 0.01 --data ../rdabase/data/NJ/NJ_2020_data.csv --shapes ../rdabase/data/NJ/NJ_2020_shapes_simplified.json --graph ../rdabase/data/NJ/NJ_2020_graph.json --output temp/NJ20C_random_plan.csv --log temp/NJ20C_random_log.txt --no-debug
echo 'Running NJ upper 40 ...'
scripts/random_map.py --state NJ --plantype upper --roughlyequal 0.1 --data ../rdabase/data/NJ/NJ_2020_data.csv --shapes ../rdabase/data/NJ/NJ_2020_shapes_simplified.json --graph ../rdabase/data/NJ/NJ_2020_graph.json --output temp/NJ20U_random_plan.csv --log temp/NJ20U_random_log.txt --no-debug
echo 'Running NM congress 3 ...'
scripts/random_map.py --state NM --plantype congress --roughlyequal 0.01 --data ../rdabase/data/NM/NM_2020_data.csv --shapes ../rdabase/data/NM/NM_2020_shapes_simplified.json --graph ../rdabase/data/NM/NM_2020_graph.json --output temp/NM20C_random_plan.csv --log temp/NM20C_random_log.txt --no-debug
echo 'Running NM upper 42 ...'
scripts/random_map.py --state NM --plantype upper --roughlyequal 0.1 --data ../rdabase/data/NM/NM_2020_data.csv --shapes ../rdabase/data/NM/NM_2020_shapes_simplified.json --graph ../rdabase/data/NM/NM_2020_graph.json --output temp/NM20U_random_plan.csv --log temp/NM20U_random_log.txt --no-debug
echo 'Running NM lower 70 ...'
scripts/random_map.py --state NM --plantype lower --roughlyequal 0.1 --data ../rdabase/data/NM/NM_2020_data.csv --shapes ../rdabase/data/NM/NM_2020_shapes_simplified.json --graph ../rdabase/data/NM/NM_2020_graph.json --output temp/NM20L_random_plan.csv --log temp/NM20L_random_log.txt --no-debug
echo 'Running NY congress 26 ...'
# scripts/random_map.py --state NY --plantype congress --roughlyequal 0.01 --data ../rdabase/data/NY/NY_2020_data.csv --shapes ../rdabase/data/NY/NY_2020_shapes_simplified.json --graph ../rdabase/data/NY/NY_2020_graph.json --output temp/NY20C_random_plan.csv --log temp/NY20C_random_log.txt --no-debug
echo 'Running NY upper 63 ...'
# scripts/random_map.py --state NY --plantype upper --roughlyequal 0.1 --data ../rdabase/data/NY/NY_2020_data.csv --shapes ../rdabase/data/NY/NY_2020_shapes_simplified.json --graph ../rdabase/data/NY/NY_2020_graph.json --output temp/NY20U_random_plan.csv --log temp/NY20U_random_log.txt --no-debug
echo 'Running NY lower 150 ...'
# scripts/random_map.py --state NY --plantype lower --roughlyequal 0.1 --data ../rdabase/data/NY/NY_2020_data.csv --shapes ../rdabase/data/NY/NY_2020_shapes_simplified.json --graph ../rdabase/data/NY/NY_2020_graph.json --output temp/NY20L_random_plan.csv --log temp/NY20L_random_log.txt --no-debug
echo 'Running NC congress 14 ...'
scripts/random_map.py --state NC --plantype congress --roughlyequal 0.01 --data ../rdabase/data/NC/NC_2020_data.csv --shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json --graph ../rdabase/data/NC/NC_2020_graph.json --output temp/NC20C_random_plan.csv --log temp/NC20C_random_log.txt --no-debug
echo 'Running NC upper 50 ...'
scripts/random_map.py --state NC --plantype upper --roughlyequal 0.1 --data ../rdabase/data/NC/NC_2020_data.csv --shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json --graph ../rdabase/data/NC/NC_2020_graph.json --output temp/NC20U_random_plan.csv --log temp/NC20U_random_log.txt --no-debug
echo 'Running NC lower 120 ...'
scripts/random_map.py --state NC --plantype lower --roughlyequal 0.1 --data ../rdabase/data/NC/NC_2020_data.csv --shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json --graph ../rdabase/data/NC/NC_2020_graph.json --output temp/NC20L_random_plan.csv --log temp/NC20L_random_log.txt --no-debug
echo 'Running ND upper 47 ...'
# scripts/random_map.py --state ND --plantype upper --roughlyequal 0.1 --data ../rdabase/data/ND/ND_2020_data.csv --shapes ../rdabase/data/ND/ND_2020_shapes_simplified.json --graph ../rdabase/data/ND/ND_2020_graph.json --output temp/ND20U_random_plan.csv --log temp/ND20U_random_log.txt --no-debug
echo 'Running ND lower 49 ...'
# scripts/random_map.py --state ND --plantype lower --roughlyequal 0.1 --data ../rdabase/data/ND/ND_2020_data.csv --shapes ../rdabase/data/ND/ND_2020_shapes_simplified.json --graph ../rdabase/data/ND/ND_2020_graph.json --output temp/ND20L_random_plan.csv --log temp/ND20L_random_log.txt --no-debug
echo 'Running OH congress 15 ...'
scripts/random_map.py --state OH --plantype congress --roughlyequal 0.01 --data ../rdabase/data/OH/OH_2020_data.csv --shapes ../rdabase/data/OH/OH_2020_shapes_simplified.json --graph ../rdabase/data/OH/OH_2020_graph.json --output temp/OH20C_random_plan.csv --log temp/OH20C_random_log.txt --no-debug
echo 'Running OH upper 33 ...'
scripts/random_map.py --state OH --plantype upper --roughlyequal 0.1 --data ../rdabase/data/OH/OH_2020_data.csv --shapes ../rdabase/data/OH/OH_2020_shapes_simplified.json --graph ../rdabase/data/OH/OH_2020_graph.json --output temp/OH20U_random_plan.csv --log temp/OH20U_random_log.txt --no-debug
echo 'Running OH lower 99 ...'
scripts/random_map.py --state OH --plantype lower --roughlyequal 0.1 --data ../rdabase/data/OH/OH_2020_data.csv --shapes ../rdabase/data/OH/OH_2020_shapes_simplified.json --graph ../rdabase/data/OH/OH_2020_graph.json --output temp/OH20L_random_plan.csv --log temp/OH20L_random_log.txt --no-debug
echo 'Running OK congress 5 ...'
# scripts/random_map.py --state OK --plantype congress --roughlyequal 0.01 --data ../rdabase/data/OK/OK_2020_data.csv --shapes ../rdabase/data/OK/OK_2020_shapes_simplified.json --graph ../rdabase/data/OK/OK_2020_graph.json --output temp/OK20C_random_plan.csv --log temp/OK20C_random_log.txt --no-debug
echo 'Running OK upper 48 ...'
# scripts/random_map.py --state OK --plantype upper --roughlyequal 0.1 --data ../rdabase/data/OK/OK_2020_data.csv --shapes ../rdabase/data/OK/OK_2020_shapes_simplified.json --graph ../rdabase/data/OK/OK_2020_graph.json --output temp/OK20U_random_plan.csv --log temp/OK20U_random_log.txt --no-debug
echo 'Running OK lower 101 ...'
# scripts/random_map.py --state OK --plantype lower --roughlyequal 0.1 --data ../rdabase/data/OK/OK_2020_data.csv --shapes ../rdabase/data/OK/OK_2020_shapes_simplified.json --graph ../rdabase/data/OK/OK_2020_graph.json --output temp/OK20L_random_plan.csv --log temp/OK20L_random_log.txt --no-debug
echo 'Running OR congress 6 ...'
# scripts/random_map.py --state OR --plantype congress --roughlyequal 0.01 --data ../rdabase/data/OR/OR_2020_data.csv --shapes ../rdabase/data/OR/OR_2020_shapes_simplified.json --graph ../rdabase/data/OR/OR_2020_graph.json --output temp/OR20C_random_plan.csv --log temp/OR20C_random_log.txt --no-debug
echo 'Running OR upper 30 ...'
# scripts/random_map.py --state OR --plantype upper --roughlyequal 0.1 --data ../rdabase/data/OR/OR_2020_data.csv --shapes ../rdabase/data/OR/OR_2020_shapes_simplified.json --graph ../rdabase/data/OR/OR_2020_graph.json --output temp/OR20U_random_plan.csv --log temp/OR20U_random_log.txt --no-debug
echo 'Running OR lower 60 ...'
# scripts/random_map.py --state OR --plantype lower --roughlyequal 0.1 --data ../rdabase/data/OR/OR_2020_data.csv --shapes ../rdabase/data/OR/OR_2020_shapes_simplified.json --graph ../rdabase/data/OR/OR_2020_graph.json --output temp/OR20L_random_plan.csv --log temp/OR20L_random_log.txt --no-debug
echo 'Running PA congress 17 ...'
scripts/random_map.py --state PA --plantype congress --roughlyequal 0.01 --data ../rdabase/data/PA/PA_2020_data.csv --shapes ../rdabase/data/PA/PA_2020_shapes_simplified.json --graph ../rdabase/data/PA/PA_2020_graph.json --output temp/PA20C_random_plan.csv --log temp/PA20C_random_log.txt --no-debug
echo 'Running PA upper 50 ...'
scripts/random_map.py --state PA --plantype upper --roughlyequal 0.1 --data ../rdabase/data/PA/PA_2020_data.csv --shapes ../rdabase/data/PA/PA_2020_shapes_simplified.json --graph ../rdabase/data/PA/PA_2020_graph.json --output temp/PA20U_random_plan.csv --log temp/PA20U_random_log.txt --no-debug
echo 'Running PA lower 203 ...'
scripts/random_map.py --state PA --plantype lower --roughlyequal 0.1 --data ../rdabase/data/PA/PA_2020_data.csv --shapes ../rdabase/data/PA/PA_2020_shapes_simplified.json --graph ../rdabase/data/PA/PA_2020_graph.json --output temp/PA20L_random_plan.csv --log temp/PA20L_random_log.txt --no-debug
echo 'Running RI congress 2 ...'
# scripts/random_map.py --state RI --plantype congress --roughlyequal 0.01 --data ../rdabase/data/RI/RI_2020_data.csv --shapes ../rdabase/data/RI/RI_2020_shapes_simplified.json --graph ../rdabase/data/RI/RI_2020_graph.json --output temp/RI20C_random_plan.csv --log temp/RI20C_random_log.txt --no-debug
echo 'Running RI upper 38 ...'
# scripts/random_map.py --state RI --plantype upper --roughlyequal 0.1 --data ../rdabase/data/RI/RI_2020_data.csv --shapes ../rdabase/data/RI/RI_2020_shapes_simplified.json --graph ../rdabase/data/RI/RI_2020_graph.json --output temp/RI20U_random_plan.csv --log temp/RI20U_random_log.txt --no-debug
echo 'Running RI lower 75 ...'
# scripts/random_map.py --state RI --plantype lower --roughlyequal 0.1 --data ../rdabase/data/RI/RI_2020_data.csv --shapes ../rdabase/data/RI/RI_2020_shapes_simplified.json --graph ../rdabase/data/RI/RI_2020_graph.json --output temp/RI20L_random_plan.csv --log temp/RI20L_random_log.txt --no-debug
echo 'Running SC congress 7 ...'
scripts/random_map.py --state SC --plantype congress --roughlyequal 0.01 --data ../rdabase/data/SC/SC_2020_data.csv --shapes ../rdabase/data/SC/SC_2020_shapes_simplified.json --graph ../rdabase/data/SC/SC_2020_graph.json --output temp/SC20C_random_plan.csv --log temp/SC20C_random_log.txt --no-debug
echo 'Running SC upper 46 ...'
scripts/random_map.py --state SC --plantype upper --roughlyequal 0.1 --data ../rdabase/data/SC/SC_2020_data.csv --shapes ../rdabase/data/SC/SC_2020_shapes_simplified.json --graph ../rdabase/data/SC/SC_2020_graph.json --output temp/SC20U_random_plan.csv --log temp/SC20U_random_log.txt --no-debug
echo 'Running SC lower 124 ...'
scripts/random_map.py --state SC --plantype lower --roughlyequal 0.1 --data ../rdabase/data/SC/SC_2020_data.csv --shapes ../rdabase/data/SC/SC_2020_shapes_simplified.json --graph ../rdabase/data/SC/SC_2020_graph.json --output temp/SC20L_random_plan.csv --log temp/SC20L_random_log.txt --no-debug
echo 'Running SD upper 35 ...'
# scripts/random_map.py --state SD --plantype upper --roughlyequal 0.1 --data ../rdabase/data/SD/SD_2020_data.csv --shapes ../rdabase/data/SD/SD_2020_shapes_simplified.json --graph ../rdabase/data/SD/SD_2020_graph.json --output temp/SD20U_random_plan.csv --log temp/SD20U_random_log.txt --no-debug
echo 'Running SD lower 37 ...'
# scripts/random_map.py --state SD --plantype lower --roughlyequal 0.1 --data ../rdabase/data/SD/SD_2020_data.csv --shapes ../rdabase/data/SD/SD_2020_shapes_simplified.json --graph ../rdabase/data/SD/SD_2020_graph.json --output temp/SD20L_random_plan.csv --log temp/SD20L_random_log.txt --no-debug
echo 'Running TN congress 9 ...'
# scripts/random_map.py --state TN --plantype congress --roughlyequal 0.01 --data ../rdabase/data/TN/TN_2020_data.csv --shapes ../rdabase/data/TN/TN_2020_shapes_simplified.json --graph ../rdabase/data/TN/TN_2020_graph.json --output temp/TN20C_random_plan.csv --log temp/TN20C_random_log.txt --no-debug
echo 'Running TN upper 33 ...'
# scripts/random_map.py --state TN --plantype upper --roughlyequal 0.1 --data ../rdabase/data/TN/TN_2020_data.csv --shapes ../rdabase/data/TN/TN_2020_shapes_simplified.json --graph ../rdabase/data/TN/TN_2020_graph.json --output temp/TN20U_random_plan.csv --log temp/TN20U_random_log.txt --no-debug
echo 'Running TN lower 99 ...'
# scripts/random_map.py --state TN --plantype lower --roughlyequal 0.1 --data ../rdabase/data/TN/TN_2020_data.csv --shapes ../rdabase/data/TN/TN_2020_shapes_simplified.json --graph ../rdabase/data/TN/TN_2020_graph.json --output temp/TN20L_random_plan.csv --log temp/TN20L_random_log.txt --no-debug
echo 'Running TX congress 38 ...'
scripts/random_map.py --state TX --plantype congress --roughlyequal 0.01 --data ../rdabase/data/TX/TX_2020_data.csv --shapes ../rdabase/data/TX/TX_2020_shapes_simplified.json --graph ../rdabase/data/TX/TX_2020_graph.json --output temp/TX20C_random_plan.csv --log temp/TX20C_random_log.txt --no-debug
echo 'Running TX upper 31 ...'
scripts/random_map.py --state TX --plantype upper --roughlyequal 0.1 --data ../rdabase/data/TX/TX_2020_data.csv --shapes ../rdabase/data/TX/TX_2020_shapes_simplified.json --graph ../rdabase/data/TX/TX_2020_graph.json --output temp/TX20U_random_plan.csv --log temp/TX20U_random_log.txt --no-debug
echo 'Running TX lower 150 ...'
scripts/random_map.py --state TX --plantype lower --roughlyequal 0.1 --data ../rdabase/data/TX/TX_2020_data.csv --shapes ../rdabase/data/TX/TX_2020_shapes_simplified.json --graph ../rdabase/data/TX/TX_2020_graph.json --output temp/TX20L_random_plan.csv --log temp/TX20L_random_log.txt --no-debug
echo 'Running UT congress 4 ...'
# scripts/random_map.py --state UT --plantype congress --roughlyequal 0.01 --data ../rdabase/data/UT/UT_2020_data.csv --shapes ../rdabase/data/UT/UT_2020_shapes_simplified.json --graph ../rdabase/data/UT/UT_2020_graph.json --output temp/UT20C_random_plan.csv --log temp/UT20C_random_log.txt --no-debug
echo 'Running UT upper 29 ...'
# scripts/random_map.py --state UT --plantype upper --roughlyequal 0.1 --data ../rdabase/data/UT/UT_2020_data.csv --shapes ../rdabase/data/UT/UT_2020_shapes_simplified.json --graph ../rdabase/data/UT/UT_2020_graph.json --output temp/UT20U_random_plan.csv --log temp/UT20U_random_log.txt --no-debug
echo 'Running UT lower 75 ...'
# scripts/random_map.py --state UT --plantype lower --roughlyequal 0.1 --data ../rdabase/data/UT/UT_2020_data.csv --shapes ../rdabase/data/UT/UT_2020_shapes_simplified.json --graph ../rdabase/data/UT/UT_2020_graph.json --output temp/UT20L_random_plan.csv --log temp/UT20L_random_log.txt --no-debug
echo 'Running VT upper 13 ...'
# scripts/random_map.py --state VT --plantype upper --roughlyequal 0.1 --data ../rdabase/data/VT/VT_2020_data.csv --shapes ../rdabase/data/VT/VT_2020_shapes_simplified.json --graph ../rdabase/data/VT/VT_2020_graph.json --output temp/VT20U_random_plan.csv --log temp/VT20U_random_log.txt --no-debug
echo 'Running VT lower 104 ...'
# scripts/random_map.py --state VT --plantype lower --roughlyequal 0.1 --data ../rdabase/data/VT/VT_2020_data.csv --shapes ../rdabase/data/VT/VT_2020_shapes_simplified.json --graph ../rdabase/data/VT/VT_2020_graph.json --output temp/VT20L_random_plan.csv --log temp/VT20L_random_log.txt --no-debug
echo 'Running VA congress 11 ...'
scripts/random_map.py --state VA --plantype congress --roughlyequal 0.01 --data ../rdabase/data/VA/VA_2020_data.csv --shapes ../rdabase/data/VA/VA_2020_shapes_simplified.json --graph ../rdabase/data/VA/VA_2020_graph.json --output temp/VA20C_random_plan.csv --log temp/VA20C_random_log.txt --no-debug
echo 'Running VA upper 40 ...'
scripts/random_map.py --state VA --plantype upper --roughlyequal 0.1 --data ../rdabase/data/VA/VA_2020_data.csv --shapes ../rdabase/data/VA/VA_2020_shapes_simplified.json --graph ../rdabase/data/VA/VA_2020_graph.json --output temp/VA20U_random_plan.csv --log temp/VA20U_random_log.txt --no-debug
echo 'Running VA lower 100 ...'
scripts/random_map.py --state VA --plantype lower --roughlyequal 0.1 --data ../rdabase/data/VA/VA_2020_data.csv --shapes ../rdabase/data/VA/VA_2020_shapes_simplified.json --graph ../rdabase/data/VA/VA_2020_graph.json --output temp/VA20L_random_plan.csv --log temp/VA20L_random_log.txt --no-debug
echo 'Running WA congress 10 ...'
# scripts/random_map.py --state WA --plantype congress --roughlyequal 0.01 --data ../rdabase/data/WA/WA_2020_data.csv --shapes ../rdabase/data/WA/WA_2020_shapes_simplified.json --graph ../rdabase/data/WA/WA_2020_graph.json --output temp/WA20C_random_plan.csv --log temp/WA20C_random_log.txt --no-debug
echo 'Running WA upper 49 ...'
# scripts/random_map.py --state WA --plantype upper --roughlyequal 0.1 --data ../rdabase/data/WA/WA_2020_data.csv --shapes ../rdabase/data/WA/WA_2020_shapes_simplified.json --graph ../rdabase/data/WA/WA_2020_graph.json --output temp/WA20U_random_plan.csv --log temp/WA20U_random_log.txt --no-debug
echo 'Running WV congress 2 ...'
# scripts/random_map.py --state WV --plantype congress --roughlyequal 0.01 --data ../rdabase/data/WV/WV_2020_data.csv --shapes ../rdabase/data/WV/WV_2020_shapes_simplified.json --graph ../rdabase/data/WV/WV_2020_graph.json --output temp/WV20C_random_plan.csv --log temp/WV20C_random_log.txt --no-debug
echo 'Running WV upper 17 ...'
# scripts/random_map.py --state WV --plantype upper --roughlyequal 0.1 --data ../rdabase/data/WV/WV_2020_data.csv --shapes ../rdabase/data/WV/WV_2020_shapes_simplified.json --graph ../rdabase/data/WV/WV_2020_graph.json --output temp/WV20U_random_plan.csv --log temp/WV20U_random_log.txt --no-debug
echo 'Running WV lower 100 ...'
# scripts/random_map.py --state WV --plantype lower --roughlyequal 0.1 --data ../rdabase/data/WV/WV_2020_data.csv --shapes ../rdabase/data/WV/WV_2020_shapes_simplified.json --graph ../rdabase/data/WV/WV_2020_graph.json --output temp/WV20L_random_plan.csv --log temp/WV20L_random_log.txt --no-debug
echo 'Running WI congress 8 ...'
scripts/random_map.py --state WI --plantype congress --roughlyequal 0.01 --data ../rdabase/data/WI/WI_2020_data.csv --shapes ../rdabase/data/WI/WI_2020_shapes_simplified.json --graph ../rdabase/data/WI/WI_2020_graph.json --output temp/WI20C_random_plan.csv --log temp/WI20C_random_log.txt --no-debug
echo 'Running WI upper 33 ...'
scripts/random_map.py --state WI --plantype upper --roughlyequal 0.1 --data ../rdabase/data/WI/WI_2020_data.csv --shapes ../rdabase/data/WI/WI_2020_shapes_simplified.json --graph ../rdabase/data/WI/WI_2020_graph.json --output temp/WI20U_random_plan.csv --log temp/WI20U_random_log.txt --no-debug
echo 'Running WI lower 99 ...'
scripts/random_map.py --state WI --plantype lower --roughlyequal 0.1 --data ../rdabase/data/WI/WI_2020_data.csv --shapes ../rdabase/data/WI/WI_2020_shapes_simplified.json --graph ../rdabase/data/WI/WI_2020_graph.json --output temp/WI20L_random_plan.csv --log temp/WI20L_random_log.txt --no-debug
echo 'Running WY upper 31 ...'
# scripts/random_map.py --state WY --plantype upper --roughlyequal 0.1 --data ../rdabase/data/WY/WY_2020_data.csv --shapes ../rdabase/data/WY/WY_2020_shapes_simplified.json --graph ../rdabase/data/WY/WY_2020_graph.json --output temp/WY20U_random_plan.csv --log temp/WY20U_random_log.txt --no-debug
echo 'Running WY lower 62 ...'
# scripts/random_map.py --state WY --plantype lower --roughlyequal 0.1 --data ../rdabase/data/WY/WY_2020_data.csv --shapes ../rdabase/data/WY/WY_2020_shapes_simplified.json --graph ../rdabase/data/WY/WY_2020_graph.json --output temp/WY20L_random_plan.csv --log temp/WY20L_random_log.txt --no-debug
