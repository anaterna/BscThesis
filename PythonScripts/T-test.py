import pandas as pd
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math


def satd_test(df, project):
    # Perform T-test on the TD
    # Split the dataset into two groups
    debt_only = df[((df['cg-npm'] == 0) & (df['cg-na'] == 0))
                   & (df['total-debt'] != 0)]
    debt_and_grime = df[((df['cg-npm'] != 0) | (df['cg-na'] != 0))
                        & (df['total-debt'] != 0)]

    # Generate the statistics for each dataset
    debt_only_stats = debt_only['total-debt'].describe()
    debt_and_grime_stats = debt_and_grime['total-debt'].describe()

    print("Info for only debt")
    print(debt_only_stats)
    print("Info where there is td and grime")
    print(debt_and_grime_stats)

    # Perform the t-test
    t_statistic, p_value = ttest_ind(
        debt_only['total-debt'], debt_and_grime['total-debt'], equal_var=False)

    print(t_statistic)
    print(p_value)

    # # Interpret the results
    alpha = 0.05  # significance level

    if p_value < alpha:
        print("There is a significant difference in the mean amount of debt between the two groups.")
    else:
        print("There is no significant difference in the mean amount of debt between the two groups.")

    # Create a box plot
    data = [debt_only['total-debt'], debt_and_grime['total-debt']]
    labels = ['SATD Only', 'SATD and Grime']
    df_box = pd.DataFrame(data=data, index=labels).T
    ax = sns.boxplot(data=df_box, showfliers=False)
    plt.xlabel('Group')
    plt.ylabel('Amount of SATD')
    fileName = f'Results/satd_t_test_{project}.png'
    plt.savefig(fileName, dpi=300)  # example path
    plt.show()


# Perform T-test on grime
# Split the dataset into two groups
def cg_na_test(df, project):
    grime_only = df[(df['cg-na'] != 0)
                    & (df['total-debt'] == 0)]
    debt_and_grime = df[(df['cg-na'] != 0) & (df['total-debt'] != 0)]

    # Perform the t-test
    t_statistic, p_value = ttest_ind(
        grime_only['cg-na'], debt_and_grime['cg-na'], equal_var=False)

    # # Generate the statistics for each dataset
    grime_only_stats = grime_only['cg-na'].describe()
    grime_and_debt_stats = debt_and_grime['cg-na'].describe()

    print("Info for only debt")
    print(grime_only_stats)
    print("Info where there is td and grime")
    print(grime_and_debt_stats)

    print(t_statistic)
    print(p_value)

    # # Interpret the results
    alpha = 0.05  # significance level

    if p_value < alpha:
        print("There is a significant difference in the mean amount of debt between the two groups.")
    else:
        print("There is no significant difference in the mean amount of debt between the two groups.")

    # Create a box plot
    data = [grime_only['cg-na'], debt_and_grime['cg-na']]
    labels = ['cg-na only', 'SATD and cg-na']
    df_box = pd.DataFrame(data=data, index=labels).T
    ax = sns.boxplot(data=df_box, showfliers=False)
    fileName = f'Results/satd_cg-na_t_test_{project}.png'
    plt.savefig(fileName, dpi=300)  # example path
    plt.xlabel('Group')
    plt.ylabel('Amount of cg-na')
    plt.show()


def cg_npm_test(df, project):
    grime_only = df[(df['cg-npm'] != 0)
                    & (df['total-debt'] == 0)]
    debt_and_grime = df[(df['cg-npm'] != 0) & (df['total-debt'] != 0)]

    # Perform the t-test
    t_statistic, p_value = ttest_ind(
        grime_only['cg-npm'], debt_and_grime['cg-npm'], equal_var=False)

    # # Generate the statistics for each dataset
    grime_only_stats = grime_only['cg-npm'].describe()
    grime_and_debt_stats = debt_and_grime['cg-npm'].describe()

    print("Info for only debt")
    print(grime_only_stats)
    print("Info where there is td and grime")
    print(grime_and_debt_stats)

    print(t_statistic)
    print(p_value)

    # # Interpret the results
    alpha = 0.05  # significance level

    if p_value < alpha:
        print("There is a significant difference in the mean amount of debt between the two groups.")
    else:
        print("There is no significant difference in the mean amount of debt between the two groups.")

    # # Create a box plot
    data = [grime_only['cg-npm'], debt_and_grime['cg-npm']]
    labels = ['cg-npm only', 'SATD and cg-npm']
    df_box = pd.DataFrame(data=data, index=labels).T
    ax = sns.boxplot(data=df_box, showfliers=False)
    fileName = f'Results/satd_cg-npm_t_test_{project}.png'
    plt.savefig(fileName, dpi=300)  # example path
    plt.xlabel('Group')
    plt.ylabel('Amount of cg-npm')
    plt.show()


def pattern_test():
    df = pd.read_csv('CSV Files/instance_grime_jhot_questdb_hbase.csv')
    current_pattern = df['Pattern'][0]
    print(current_pattern)
    pattern_data = []
    t_statistic_list = []
    p_value_list = []
    patter_names = []
    num_patterns = {}
    # Iterate through instances
    for _, row in df.iterrows():
        pattern = row['Pattern']
        # print("row file: {}".format(row['file']))
        # print("pattern: {}, current pattern: {}".format(pattern, current_pattern))

        if pattern != current_pattern:
            num_patterns[current_pattern] = len(pattern_data)

            # Perform t-test for the previous pattern
            if pattern_data:
                # print("Pattern data: {}".format(pattern_data[0]['Pattern']))
                grime_only = [d['Sum of cg-na'] for d in pattern_data if d['Sum of total-debt']
                              == 0 and d['Sum of cg-na'] != 0]
                debt_and_grime = [
                    d['Sum of cg-na'] for d in pattern_data if d['Sum of total-debt'] != 0 and d['Sum of cg-na'] != 0]
                # print(grime_only)
                # print()
                # print(debt_and_grime)

                # print(debt_and_grime)
                # Perform the t-test
                t_statistic, p_value = ttest_ind(
                    grime_only, debt_and_grime, equal_var=False)
                # check if p_value is not nan
                if not math.isnan(p_value):
                    t_statistic_list.append(t_statistic)

                    p_value_list.append(p_value)

                    patter_names.append(current_pattern)

            # Reset pattern-specific data
            current_pattern = pattern
            pattern_data = []

        # Store the instance data for the current pattern
        pattern_data.append(row)

    # Perform t-test for the last pattern
    if pattern_data:
        grime_only = [d['Sum of cg-na']
                      for d in pattern_data if d['Sum of total-debt'] == 0 and d['Sum of cg-na'] != 0]
        debt_and_grime = [d['Sum of cg-na']
                          for d in pattern_data if d['Sum of total-debt'] != 0 and d['Sum of cg-na'] != 0]

        # Perform the t-test
        t_statistic, p_value = ttest_ind(
            grime_only, debt_and_grime, equal_var=False)
        if not math.isnan(p_value):
            t_statistic_list.append(t_statistic)

            p_value_list.append(p_value)

            patter_names.append(current_pattern)

    print(patter_names)
    print(t_statistic_list)
    print(p_value_list)
    print(num_patterns)
    print()
    for i in range(len(patter_names)):
        print("{}: t_statistic: {}, p_value: {}, count: {}".format(
            patter_names[i], t_statistic_list[i], p_value_list[i], num_patterns[patter_names[i]]))

    # remove patterns and p_value and t_statistic that have nan at the same index


df = pd.read_csv('CSV Files/merged.csv')  # example
project = 'all'
# df = df[df['project'] == project]
pattern_test()

# satd_test(df, project)

# cg_na_test(df, project)

# cg_npm_test(df, project)
