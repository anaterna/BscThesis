import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('csv_files_jhotdraw/rule_occurrences.csv')

# Group the data by TDType and sum the occurrences
grouped_df = df.groupby('TDType')['Occurrences'].sum().reset_index()

# Sort the DataFrame by the summed occurrences in descending order
sorted_df = grouped_df.sort_values('Occurrences', ascending=True)

print(sorted_df['Occurrences'])
# Create the graph
plt.barh(sorted_df['TDType'], sorted_df['Occurrences'])
plt.xlabel('Number of Occurrences')
plt.ylabel('TDType')
plt.title('Distribution of Technical Debt Types')

plt.tight_layout()  # Add this line to prevent cropping of titles
# Save the figure (optional)
plt.savefig(f'charts/td_distribution_jhot.png')

# Display the graph
plt.show()

