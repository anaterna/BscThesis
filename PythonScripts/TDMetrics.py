import pandas as pd
import matplotlib.pyplot as plt
import json
from collections import defaultdict

# This script is used to extract quality metrics per project:
# and display the distribution of the metrics in a bar chart

# Create a defaultdict to store the aggregated metrics
metrics = defaultdict(int)

# List of JSON file paths
json_files = ["core"]  # Add your file paths here

# Process each JSON file
for file in json_files:
    with open(f'csv_files_questdb/{file}_metrics.json') as f:
        data = json.load(f)
        measures = data["component"]["measures"]

        # Iterate over the metrics in the JSON
        for metric in measures:
            metric_name = metric["metric"]
            metric_value = round(float(metric["value"]))
            metrics[metric_name] += metric_value
      

        # Filter metrics corresponding to technical debt
        technical_debt_metrics = ['vulnerabilities', 'bugs', 'code_smells', 'critical_violations', 'complexity']
        filtered_measures = [measure for measure in measures if measure['metric'] in technical_debt_metrics]

        # Sort the filtered measures by value in ascending order
        sorted_measures = sorted(filtered_measures, key=lambda x: float(x['value']))
        print(sorted_measures)
        # Set up the figure and axes
        fig, ax = plt.subplots(figsize=(16, 12))

        # Plot the bar chart with logarithmic scale on y-axis
        bars = ax.bar([measure['metric'] for measure in sorted_measures],
                    [float(measure['value']) for measure in sorted_measures], color='#1f77b4')

        # Set the y-axis to logarithmic scale
        ax.set_yscale('log')

        # Add value labels above each bar
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval, int(yval),
                    ha='center', va='bottom', color='black', fontsize=12)

        # Customize axis labels and title
        ax.set_xlabel('Metrics', fontsize=12)
        ax.set_ylabel('Value (Log Scale)', fontsize=12)
        ax.set_title(f'TD Metrics for Project: {file}', fontsize=14, fontweight='bold')

        # Customize tick labels
        plt.xticks(fontsize=10, rotation=45)
        plt.yticks(fontsize=10)

        # Customize grid lines
        ax.grid(axis='y', linestyle='--', linewidth=0.5)

        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Save the figure (optional)
        plt.savefig(f'charts/{file}_bar_chart.png', dpi=300)

        # Show the graph
        plt.show()


# Print the aggregated metrics
for metric_name, metric_value in metrics.items():
    print(f"{metric_name}: {metric_value}")

# Extract x and y data from the dictionary
x = list(metrics.keys())
y = list(metrics.values())


# Set up the figure and axes
fig, ax = plt.subplots(figsize=(16, 12))

# Plot the bar chart with logarithmic scale on y-axis
bars = ax.bar(x, y, color='#1f77b4')

# Set the y-axis to logarithmic scale
ax.set_yscale('log')

# Add value labels above each bar
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval, int(yval),
            ha='center', va='bottom', color='black', fontsize=12)

# Customize axis labels and title
ax.set_xlabel('Metrics', fontsize=12)
ax.set_ylabel('Value (Log Scale)', fontsize=12)
ax.set_title('Total TD Metrics for Repository questdb', fontsize=14, fontweight='bold')

# Customize tick labels
plt.xticks(fontsize=10, rotation=45)
plt.yticks(fontsize=10)

# Customize grid lines
ax.grid(axis='y', linestyle='--', linewidth=0.5)

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)



# Save the figure (optional)
plt.savefig(f'charts/total_bar_chart.png', dpi=300)

# Show the graph
plt.show()