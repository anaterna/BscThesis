import pandas as pd
import matplotlib.pyplot as plt
import json

# # Read in the CSV file
# df = pd.read_csv('csv_files/rule_occurrences.csv')

# # Create a chart showing the distribution of technical debt per package
# package_debt = df.groupby('Class')['RuleId'].count()
# package_debt.plot(kind='barh', figsize=(8, 10))
# plt.title('Technical Debt Distribution by Package')
# plt.xlabel('Number of Instances')
# plt.ylabel('Package')
# plt.show()

# Create a chart showing the most common technical debt instances and the number of classes where they were detected
# rule_count = df.groupby('RuleId')['Class'].nunique().sort_values(ascending=False)
# # Drop insignificant rules, keep only the top 40%
# rule_count = rule_count[rule_count > 10]

# rule_count.plot(kind='barh', figsize=(10, 8))
# plt.title('Most Common Technical Debt Instances')
# plt.xlabel('Total Number of Rule Vioaltions')
# plt.ylabel('Rules')
# plt.savefig(f'charts/rules.png', dpi=300)
# plt.show()


# For top 10 rules, create a chart showing the distribution of technical debt per package
# top_10_rules = rule_count.head(10).index.tolist()
# top_10_rules_df = df[df['RuleId'].isin(top_10_rules)]
# top_10_rules_df = top_10_rules_df.groupby(['RuleId', 'Class'])['RuleId'].count().unstack('RuleId').fillna(0)
# top_10_rules_df.plot(kind='barh', stacked=True, figsize=(10, 8))
# plt.title('Technical Debt Distribution by Package')
# plt.xlabel('Number of Instances')
# plt.ylabel('Package')
# plt.savefig(f'charts/rules_by_package.png', dpi=300)
# plt.show()



# # Extract RuleId and Occurrences columns
# df = df.sort_values('Occurrences', ascending=False)

# # Calculate the threshold for the top 40% rules
# top_percent = 0.4
# threshold = int(len(df) * top_percent)

# # Extract RuleId and Occurrences columns for the top rules
# top_rules = df[:threshold]
# rule_ids = top_rules['RuleId']
# occurrences = top_rules['Occurrences']

# # Create a horizontal bar graph
# plt.figure(figsize=(10, 8))
# plt.barh(rule_ids, occurrences)
# plt.xlabel('Nr. of Occurrences')
# plt.ylabel('Rule Id')
# plt.title('Top 40% Occurrences of Rule Ids in JHotDraw Project')

# # Invert the y-axis to display the highest occurrence on top
# plt.gca().invert_yaxis()

# # Save the graph as an image file (e.g., PNG)
# plt.savefig('rule_occurrences_graph_jhotdraw.png')

# # Show the graph
# plt.show()


# Plot pattern statistics
data = pd.read_csv('FINAL_QDB/pattern_grime.csv')

# Discard specific columns from the DataFrame
columns_to_discard = ['Minor', 'Major', 'Critical']  # Specify the columns you want to discard
data = data.drop(columns_to_discard, axis=1)


# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Set the Pattern column as the index and sort patterns based on the sum of the columns
df.set_index('Pattern', inplace=True)
df['Sum'] = df.sum(axis=1)
df = df.sort_values(by='Sum', ascending=True)

# Remove the Sum column
df.drop('Sum', axis=1, inplace=True)

# Plot the horizontal stacked bar chart
ax = df.plot(kind='barh', stacked=True, figsize=(10, 6))
ax.set_xlabel('Metric Value')
ax.set_ylabel('Pattern')
ax.legend(title='Metric')

plt.savefig(f'Results/patterns_distr_qdb.png', dpi=300)
# Display the plot
plt.show()