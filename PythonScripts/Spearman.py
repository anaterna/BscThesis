import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.stats import spearmanr
# Load the data into a DataFrame
data = pd.read_csv("./FINAL_QDB/MultipleInstanceGrimeClasses/multiple_merged_files.csv")


grime_metrics = ['cg-na', 'cg-npm']
quality_attributes = ['TD', 'Minor', 'Major', 'Critical']

# Rename the 'TotalBrokenRules' column to 'TD'
data = data.rename(columns={'TotalBrokenRules': 'TD'})

# Select the relevant data subset
subset_data = data[quality_attributes + grime_metrics]

# Compute the correlation matrix
corr, _ = spearmanr(subset_data)


# Remove the rows except the first four
corr = corr[0:4, 4:]

# Create a DataFrame from the correlation matrix
corr_df = pd.DataFrame(corr, columns=grime_metrics, index=quality_attributes)



# Define the correlation guideline thresholds
thresholds = [0.00, 0.20, 0.40, 0.60, 0.80, 1.00]
labels = ['very weak', 'weak', 'moderate', 'strong', 'very strong']

# Create a custom colormap with the desired color ranges for each threshold
colors = ['#f2f2f2', '#e0f2f9', '#bae4bc', '#7bccc4', '#2b8cbe']
cmap = sns.color_palette(colors)

# Compute the absolute correlation matrix
# Compute the absolute correlation matrix
abs_corr = np.abs(corr)

# Initialize the matplotlib figure and axes
fig, ax = plt.subplots(figsize=(6, 4))

# Draw the heatmap with the colorbar
# Allow negative correlations and set the color range from 0 to 1 but keep the negative values
sns.heatmap(abs_corr, vmin=0, vmax=1, cmap=cmap, annot=corr_df, fmt='.2f', linewidths=0.5, cbar=True)

# Set the variable names as labels
ax.set_xticklabels(grime_metrics, rotation=45, ha='right', fontsize=10)
ax.set_yticklabels(quality_attributes[::-1], rotation=0, ha='right', fontsize=10)

# Set the general x and y axis labels
ax.set_xlabel('Grime metrics', fontsize=12)
ax.set_ylabel('Technical debt', fontsize=12)

# Add the correlation guidelines in a separate legend box
legend_handles = []

j = 0

for i, color in enumerate(colors):

    legend_handles.append(plt.Rectangle((0, 0), 1, 1, fc=color))

ax.legend(legend_handles, labels, bbox_to_anchor=(1.55, 0.5), loc='center', ncol=1)
# Adjust the layout to prevent cutoff of tick labels and legend
plt.tight_layout(rect=[0, 0.15, 1, 1])

# Show the heatmap
plt.savefig(f'Results/spearman_class_qdb_multiple_.png', dpi=300)