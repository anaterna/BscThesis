import pandas as pd
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math


def satd_test(df, project):
    # Perform T-test on the TD
    # Split the dataset into two groups
    debt_only = df[((df['mg-ce'] == 0) & (df['mg-ca'] == 0))
                   & (df['Sum of total-debt'] != 0)]

    debt_and_grime = df[((df['mg-ce'] != 0) | (df['mg-ca'] != 0))
                        & (df['Sum of total-debt'] != 0)]

    # # Generate the statistics for each dataset
    debt_only_stats = debt_only['Sum of total-debt'].describe()
    debt_and_grime_stats = debt_and_grime['Sum of total-debt'].describe()

    print("Info for only debt")
    print(debt_only_stats)
    print("Info where there is td and grime")
    print(debt_and_grime_stats)

    # Perform the t-test
    t_statistic, p_value = ttest_ind(
        debt_only['Sum of total-debt'], debt_and_grime['Sum of total-debt'], equal_var=False)

    print(t_statistic)
    print(p_value)

    # Interpret the results
    alpha = 0.05  # significance level

    if p_value < alpha:
        print("There is a significant difference in the mean amount of debt between the two groups.")
    else:
        print("There is no significant difference in the mean amount of debt between the two groups.")

    # Create a box plot
    data = [debt_only['Sum of total-debt'],
            debt_and_grime['Sum of total-debt']]
    labels = ['SATD Only', 'SATD and Grime']
    df_box = pd.DataFrame(data=data, index=labels).T
    ax = sns.boxplot(data=df_box, showfliers=False)
    plt.xlabel('Group')
    plt.ylabel('Amount of SATD')
    fileName = f'Results/satd_mod_t_test_{project}.png'
    plt.savefig(fileName, dpi=300)  # example path
    plt.show()


def mg_ce_test(df, project):
    # Perform T-test on grime
    # Split the dataset into two groups
    grime_only = df[(df['mg-ce'] != 0)
                    & (df['Sum of total-debt'] == 0)]
    debt_and_grime = df[(df['mg-ce'] != 0) & (df['Sum of total-debt'] != 0)]

    # Perform the t-test
    t_statistic, p_value = ttest_ind(
        grime_only['mg-ce'], debt_and_grime['mg-ce'], equal_var=False)

    # # Generate the statistics for each dataset
    grime_only_stats = grime_only['mg-ce'].describe()
    grime_and_debt_stats = debt_and_grime['mg-ce'].describe()

    print("Info for only grime")
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
    data = [grime_only['mg-ce'], debt_and_grime['mg-ce']]
    labels = ['mg-ce only', 'SATD and mg-ce']
    df_box = pd.DataFrame(data=data, index=labels).T
    ax = sns.boxplot(data=df_box, showfliers=False)
    fileName = f'Results/satd_mg-ce_t_test_{project}.png'
    plt.savefig(fileName, dpi=300)  # example path
    plt.xlabel('Group')
    plt.ylabel('Amount of mg-ce')
    plt.show()


def mg_ca_test(df, project):
    grime_only = df[(df['mg-ca'] != 0)
                    & (df['Sum of total-debt'] == 0)]
    debt_and_grime = df[(df['mg-ca'] != 0) & (df['Sum of total-debt'] != 0)]

    # Perform the t-test
    t_statistic, p_value = ttest_ind(
        grime_only['mg-ca'], debt_and_grime['mg-ca'], equal_var=False)

    # # Generate the statistics for each dataset
    grime_only_stats = grime_only['mg-ca'].describe()
    grime_and_debt_stats = debt_and_grime['mg-ca'].describe()

    print("Info for only grime")
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
    data = [grime_only['mg-ca'], debt_and_grime['mg-ca']]
    labels = ['mg-ca only', 'SATD and mg-ca']
    df_box = pd.DataFrame(data=data, index=labels).T
    ax = sns.boxplot(data=df_box, showfliers=False)
    fileName = f'Results/satd_mg-ca_t_test_{project}.png'
    plt.savefig(fileName, dpi=300)  # example path
    plt.xlabel('Group')
    plt.ylabel('Amount of mg-ca')
    plt.show()


project = 'questdb'

df = []
match project:
    case 'all':
        df = pd.read_csv(
            'CSV Files/instance_grime_jhot_questdb_hbase.csv')  # example
    case 'hbase':
        df = pd.read_csv('CSV Files/instance_grime_hbase.csv')
    case 'jhotdraw':
        df = pd.read_csv('CSV Files/instance_grime_jhotdraw.csv')
    case 'questdb':
        df = pd.read_csv('CSV Files/instance_grime_questdb.csv')
    case 'jhot_questdb':
        df = pd.read_csv('CSV Files/instance_grime_jhot_questdb.csv')
    case _:
        print('No project selected')
        exit(1)

# satd_test(df, project)
mg_ce_test(df, project)
mg_ca_test(df, project)
