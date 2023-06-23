import pandas as pd
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('./State_grime.csv') # example

# # Perform T-test on the TD
# # Split the dataset into two groups
# debt_only = df[((df['cg-npm'] == 0)) & (df['TotalBrokenRules'] != 0)]
# debt_and_grime = df[((df['cg-npm'] != 0)) & (df['TotalBrokenRules'] != 0)]

# # Generate the statistics for each dataset
# debt_only_stats = debt_only['TotalBrokenRules'].describe()
# debt_and_grime_stats = debt_and_grime['TotalBrokenRules'].describe()

# print("Info for only debt")
# print(debt_only_stats)
# print("Info where there is td and grime")
# print(debt_and_grime_stats)


# # Perform the t-test
# t_statistic, p_value = ttest_ind(debt_only['TotalBrokenRules'], debt_and_grime['TotalBrokenRules'], equal_var=False)

# print(t_statistic)
# print(p_value)

# # Interpret the results
# alpha = 0.05  # significance level

# if p_value < alpha:
#     print("There is a significant difference in the mean amount of debt between the two groups.")
# else:
#     print("There is no significant difference in the mean amount of debt between the two groups.")


# # Create a box plot
# data = [debt_only['TD'], debt_and_grime['TotalBrokenRules']]
# labels = ['TD Only', 'TD and Grime']
# df_box = pd.DataFrame(data=data, index=labels).T
# ax = sns.boxplot(data=df_box, showfliers=False)
# plt.xlabel('Group')
# plt.ylabel('Amount of TD')
# # plt.savefig(f'Results/debt_t_test_jhot_qdb.png', dpi=300) # example path
# plt.show()








# current_pattern = df['Pattern'][0]
# pattern_data = []
# t_statistic_list = []
# p_value_list = []
# patter_names = []

# # Iterate through instances
# for _, row in df.iterrows():
#     pattern = row['Pattern']
    
#     if pattern != current_pattern:
    
#         # Perform t-test for the previous pattern
#         if pattern_data:
#             grime_only = [d['cg-npm'] for d in pattern_data if d['TD'] == 0 and d['cg-npm'] != 0]
#             debt_and_grime = [d['cg-npm'] for d in pattern_data if d['TD'] != 0 and d['cg-npm'] != 0]
           
#             # Perform the t-test
#             t_statistic, p_value = ttest_ind(grime_only, debt_and_grime, equal_var=False)
#             # check if p_value is not nan
#             if not math.isnan(p_value):
#                 t_statistic_list.append(t_statistic)
                
#                 p_value_list.append(p_value)
                
#                 patter_names.append(current_pattern)        

            
#         # Reset pattern-specific data
#         current_pattern = pattern
#         pattern_data = []
    
#     # Store the instance data for the current pattern
#     pattern_data.append(row)

# # Perform t-test for the last pattern
# if pattern_data:
#     grime_only = [d['cg-npm'] for d in pattern_data if d['TD'] == 0 and d['cg-npm'] != 0]
#     debt_and_grime = [d['cg-npm'] for d in pattern_data if d['TD'] != 0 and d['cg-npm'] != 0]
    
#     # Perform the t-test
#     t_statistic, p_value = ttest_ind(grime_only, debt_and_grime, equal_var=False)
#     if not math.isnan(p_value):
#         t_statistic_list.append(t_statistic)
    
#         p_value_list.append(p_value)
        
#         patter_names.append(current_pattern)       



# print(patter_names)
# print(t_statistic_list)
# print(p_value_list)


import pandas as pd
from scipy.stats import ttest_ind

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('./CommonFiles/all_merged_files.csv')

# Filter the DataFrame based on the 'Pattern' column
subdataset = df[df['Pattern'] == '(Object)Adapter']

# Create two groups: TD only and TD + grime (cg-na)
group_td = subdataset[(subdataset['TotalBrokenRules'] != 0) & (subdataset['cg-na'] == 0) & (subdataset['cg-npm'] == 0)]
group_td_grime = subdataset[(subdataset['TotalBrokenRules'] != 0) & ((subdataset['cg-na'] != 0) | (subdataset['cg-npm'] != 0))]

# Calculate the means of TD for each group
mean_td_td = group_td['TotalBrokenRules'].mean()
mean_td_grime = group_td_grime['TotalBrokenRules'].mean()

# Perform the t-test
t_statistic, p_value = ttest_ind(group_td['TotalBrokenRules'], group_td_grime['TotalBrokenRules'])

# Print the means and t-test results
print(f"Mean of TD (TD only): {mean_td_td}")
print(f"Mean of TD (TD + grime): {mean_td_grime}")
print(f"T-Statistic: {t_statistic}")
print(f"P-value: {p_value}")