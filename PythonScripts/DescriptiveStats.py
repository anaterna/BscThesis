import pandas as pd

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('./csv_files_jhotdraw/aggregated_file.csv')

# Calculate statistics for 'cg-na'
cg_na_max = df['Info'].max()
cg_na_min = df['Info'].min()
cg_na_mean = df['Info'].mean()
cg_na_std = df['Info'].std()



# Print the statistics
print("Statistics for 'cg-na':")
print("Max:", cg_na_max)
print("Min:", cg_na_min)
print("Mean:", cg_na_mean)
print("Standard Deviation:", cg_na_std)
print()

