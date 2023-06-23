import pandas as pd
import csv

# This script is used to aggregate the data from a CSV file that contains the technical debt count per class of an entire project 

df = pd.read_csv('csv_files_hbase/all_classes_and_rules.csv')


# Create a pivot table to aggregate the data
aggregated_df = df.pivot_table(index='Class', columns='RuleId', aggfunc='size', fill_value=0)

# Add columns for severity levels
aggregated_df['Minor'] = df[df['Severity'] == 'MINOR'].groupby('Class').size()
aggregated_df['Major'] = df[df['Severity'] == 'MAJOR'].groupby('Class').size()
aggregated_df['Critical'] = df[df['Severity'] == 'CRITICAL'].groupby('Class').size()
aggregated_df['Info'] = df[df['Severity'] == 'INFO'].groupby('Class').size()

# Calculate TotalBrokenRules as the sum of RuleId columns
aggregated_df['TotalBrokenRules'] = aggregated_df.drop(['Minor', 'Major', 'Critical', 'Info'], axis=1).sum(axis=1)

# Fill missing values with 0
aggregated_df = aggregated_df.fillna(0)

# Reset the index and rename columns
aggregated_df = aggregated_df.reset_index()
aggregated_df.columns.name = None

# Reorder columns with TotalBrokenRules as the first column
column_order = ['Class', 'TotalBrokenRules', 'Minor', 'Major', 'Critical', 'Info'] 
aggregated_df = aggregated_df[column_order]


# Save the aggregated data to a new .csv file
aggregated_df.to_csv('csv_files_hbase/aggregated_TD.csv', index=False)



# Calculate the number of occurrences of each rule in the entire project
# df = pd.read_csv('csv_files_hbase/aggregated_TD.csv')

# rule_occurrences = df.groupby(['RuleId', 'RuleName']).size().reset_index(name='Occurrences')

# rule_occurrences = rule_occurrences.sort_values(by='Occurrences', ascending=False)

# # Save the rule occurrences to a new .csv file
# rule_occurrences.to_csv('csv_files_questdb/core_rule_occurrences.csv', index=False)