#!/usr/bin/env python3


import pandas as pd
import matplotlib.pyplot as plt

#

scores_dir: str = "../../iCloud/fileout/tradeoffs/NC/ensembles/"
scores_csv: str = "NC20C_scores_more.csv"
x_col: str = "efficiency_gap"
y_col: str = "alt_opportunity_districts_pct"

# Read the CSV file
df = pd.read_csv(scores_dir + scores_csv)

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(df[x_col], df[y_col], alpha=0.5)

# Set labels and title
plt.xlabel("Efficiency Gap")
plt.ylabel("Alternative Opportunity Districts %")
plt.title("Efficiency Gap vs Alternative Opportunity Districts")

# Add a grid for better readability
plt.grid(True, linestyle="--", alpha=0.7)

# Show the plot
plt.tight_layout()
plt.show()

# Optionally, save the plot as an image file
# plt.savefig('efficiency_gap_scatter_plot.png', dpi=300, bbox_inches='tight')

pass
