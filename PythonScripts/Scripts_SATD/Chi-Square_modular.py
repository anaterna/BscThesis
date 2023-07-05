import pandas as pd
from scipy.stats import kstest
from scipy.stats import chi2_contingency
# Read the CSV file into a DataFrame
df = pd.read_csv('CSV Files/instance_grime_questdb.csv')

# Create a new column "hasTD" based on 'Sum of total-debt"
df['hasTD'] = df['Sum of total-debt'].apply(lambda x: 1 if x > 0 else 0)

# Create a new column "hasModGrime" based on "mg-ca" and "mg-ce"
df['hasModGrime'] = df['mg-ca'].apply(lambda x: 1 if x >
                                      0 else 0) | df['mg-ce'].apply(lambda x: 1 if x > 0 else 0)


# Create a contingency table from the 'hasGrime' and 'hasTD' columns
contingency_table = pd.crosstab(df['hasTD'], df['hasModGrime'])

# Perform the chi-square test
chi2, p_value, dof, expected = chi2_contingency(contingency_table)

# Print the results
print('mg-ce or mg-ca')
print('Chi-square statistic:', chi2)
print('P-value:', p_value)


df['hasCA'] = df['mg-ca'].apply(lambda x: 1 if x > 0 else 0)

# Create a contingency table from the 'hasGrime' and 'hasTD' columns
contingency_table = pd.crosstab(df['hasTD'], df['hasCA'])

# Perform the chi-square test
chi2, p_value, dof, expected = chi2_contingency(contingency_table)

# Print the results

print('mg-ca')
print('Chi-square statistic:', chi2)
print('P-value:', p_value)


df['hasCE'] = df['mg-ce'].apply(lambda x: 1 if x > 0 else 0)

# Create a contingency table from the 'hasGrime' and 'hasTD' columns
contingency_table = pd.crosstab(df['hasTD'], df['hasCE'])

# Perform the chi-square test
chi2, p_value, dof, expected = chi2_contingency(contingency_table)

# Print the results

print('mg-ce')
print('Chi-square statistic:', chi2)
print('P-value:', p_value)
