import pandas as pd
import csv

df = pd.read_csv('CSV Files/merged.csv')
df = df[df['project'] == 'jhotdraw']

satd_col = df["total-debt"]

satd_stats = satd_col.describe()

print(satd_stats)

df = pd.read_csv('CSV Files/merged.csv')
df = df[df['project'] == 'questdb']

satd_col = df["total-debt"]

satd_stats = satd_col.describe()

print(satd_stats)
