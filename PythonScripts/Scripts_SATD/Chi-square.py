import pandas as pd
from scipy.stats import kstest
from scipy.stats import chi2_contingency
# Read the CSV file into a DataFrame
df = pd.read_csv('CSV Files/merged.csv')

# Create a new column "hasTD" based on "total-debt"
df['hasTD'] = df['total-debt'].apply(lambda x: 1 if x > 0 else 0)


# Create a new column "hasG" based on "cg-na and cg-npm"
df['hasG'] = df['cg-na'].apply(lambda x: 1 if x >
                               0 else 0) | df['cg-npm'].apply(lambda x: 1 if x > 0 else 0)

# Create a contingency table from the 'hasGrime' and 'hasTD' columns
contingency_table = pd.crosstab(df['hasTD'], df['hasG'])

# Perform the chi-square test
chi2, p_value, dof, expected = chi2_contingency(contingency_table)

# Print the results
print('Common files: ')
print('cg-na and cg-npm')
print('Chi-square statistic:', chi2)
print('P-value:', p_value)
print()

# create a new column, hasG based on only cg-na
df['hasG'] = df['cg-na'].apply(lambda x: 1 if x > 0 else 0)

# Create a contingency table from the 'hasGrime' and 'hasTD' columns
contingency_table = pd.crosstab(df['hasTD'], df['hasG'])

# Perform the chi-square test
chi2, p_value, dof, expected = chi2_contingency(contingency_table)

# Print the results
print('Common files: ')
print('cg-na')
print('Chi-square statistic:', chi2)
print('P-value:', p_value)
print()

# create a new column, hasG based on only cg-na
df['hasG'] = df['cg-npm'].apply(lambda x: 1 if x > 0 else 0)

# Create a contingency table from the 'hasGrime' and 'hasTD' columns
contingency_table = pd.crosstab(df['hasTD'], df['hasG'])

# Perform the chi-square test
chi2, p_value, dof, expected = chi2_contingency(contingency_table)

# Print the results
print('Common files: ')
print('cg-npm')
print('Chi-square statistic:', chi2)
print('P-value:', p_value)
print()
