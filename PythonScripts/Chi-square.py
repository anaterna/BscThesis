import pandas as pd
from scipy.stats import kstest
from scipy.stats import chi2_contingency
# Read the CSV file into a DataFrame
data = pd.read_csv('./instance_grime.csv')

# Perform the Kolmogorov-Smirnov test on TD
# stat, p_value = kstest(data['TD'], 'norm')
# print(f'Kolmogorov-Smirnov Test - TD: statistic={stat:.4f}, p-value={p_value}')

# # Perform the Kolmogorov-Smirnov test on mg-ca
# stat, p_value = kstest(data['mg-ca'], 'norm')
# print(f'Kolmogorov-Smirnov Test - mg-ca: statistic={stat:.4f}, p-value={p_value}')

# # Perform the Kolmogorov-Smirnov test on mg-ce
# stat, p_value = kstest(data['mg-ce'], 'norm')
# print(f'Kolmogorov-Smirnov Test - mg-ce: statistic={stat:.4f}, p-value={p_value}')


# Create a new column "hasTD" based on "TD"

def chi_square(df):
    df['TD'] = pd.to_numeric(df['TD'])
    df['hasTD'] = df['TD'].apply(lambda x: 1 if x > 0 else 0)

    # Create a new column "hasCA" based on "mg-ca"
    df['mg-ca'] = pd.to_numeric(df['mg-ca'])
    df['hasCA'] = df['mg-ca'].apply(lambda x: 1 if x > 0 else 0)

    # Create a new column "hasCE" based on "mg-ce"
    df['mg-ce'] = pd.to_numeric(df['mg-ce'])
    df['hasCE'] = df['mg-ce'].apply(lambda x: 1 if x > 0 else 0)

    # Create a contingency table from the 'hasGrime' and 'hasTD' columns
    contingency_table = pd.crosstab(df['hasTD'], df['hasCA'])

    # Perform the chi-square test
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)

    # Print the results
    print('mg-ca')
    print('Chi-square statistic:', chi2)
    print('P-value:', p_value)


    # Create a contingency table from the 'hasGrime' and 'hasTD' columns
    contingency_table = pd.crosstab(df['hasTD'], df['hasCE'])

    # Perform the chi-square test
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)

    # Print the results

    print('mg-ce')
    print('Chi-square statistic:', chi2)
    print('P-value:', p_value)



    # Create a new column "hasCA" based on "cg-na"
    df['cg-na'] = pd.to_numeric(df['cg-na'])
    df['hasNA'] = df['cg-na'].apply(lambda x: 1 if x > 0 else 0)

    # Create a new column "hasCE" based on "cg-npm"
    df['cg-npm'] = pd.to_numeric(df['cg-npm'])
    df['hasNPM'] = df['cg-npm'].apply(lambda x: 1 if x > 0 else 0)

    # Create a contingency table from the 'hasGrime' and 'hasTD' columns
    contingency_table = pd.crosstab(df['hasTD'], df['hasNA'])

    # Perform the chi-square test
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)

    # Print the results
    print('cg-na')
    print('Chi-square statistic:', chi2)
    print('P-value:', p_value)


    # Create a contingency table from the 'hasGrime' and 'hasTD' columns
    contingency_table = pd.crosstab(df['hasTD'], df['hasNPM'])

    # Perform the chi-square test
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)

    # Print the results

    print('cg-npm')
    print('Chi-square statistic:', chi2)
    print('P-value:', p_value)



current_pattern = data['Pattern'][0]
pattern_data = []
t_statistic_list = []
p_value_list = []
patter_names = []

# Iterate through instances
for _, row in data.iterrows():
    pattern = row['Pattern']
    
    if pattern != current_pattern:
    
        # Perform t-test for the previous pattern
        if pattern_data:
            # Perform the chi-square test
            print("-------------------")
            print(current_pattern)
            df = pd.DataFrame(pattern_data)
            chi_square(df)
            
            
        # Reset pattern-specific data
        current_pattern = pattern
        pattern_data = []
    
    # Store the instance data for the current pattern
    pattern_data.append(row)

# Perform t-test for the last pattern
if pattern_data:
    # Perform the chi-square test
    print("-------------------")
    print(current_pattern)
    df = pd.DataFrame(pattern_data)
    chi_square(df)      



