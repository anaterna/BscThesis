import pandas as pd
from os import path, stat
import csv

# Ask the user for the project name
print("Enter Project Name: ")
project = input().lower()

grime_csv = project + '_grime.csv'
grime_csv = 'CSV Files/' + grime_csv

# Check if the grime file exists
if not path.exists(grime_csv):
    print("Grime file does not exist")
    exit()


def satd_file_in_grime(satd_file, grime_file_col):
    for i in range(len(grime_file_col)):
        if satd_file == grime_file_col[i]:
            return i
    return -1


with open("merged.csv", "a+") as merged:
    satd_and_td = pd.read_csv("combined_file.csv")
    grime = pd.read_csv(grime_csv)
    # needed columns
    project_col = satd_and_td['project']
    satd_file_col = satd_and_td['file']
    grime_file_col = grime['Class']

    # Create the writer
    writer = csv.writer(merged)

    if stat("merged.csv").st_size == 0:
        # Add the columns from satd_and_td and grime to the merged file
        # there's probably a better way to do this but this works
        writer.writerow(['project', 'file', 'code|design-debt', 'requirement-debt', 'documentation-debt',
                        'test-debt', 'total-debt', 'TotalBrokenRules', 'Minor', 'Major', 'Critical', 'Info', 'cg-na', 'cg-npm', 'Pattern', 'count'])
    for i in range(len(project_col)):
        # Wrong project, dont do anything
        if project_col[i] != project:
            continue

        # Get the satd file
        satd_file = satd_file_col[i]

        # Remove the .java extension from the module names of the satd_file_col
        satd_file = satd_file.split('.')
        satd_file = satd_file[:-1]
        satd_file = '.'.join(satd_file)
        index = satd_file_in_grime(satd_file, grime_file_col)
        if index != -1:
            writer.writerow([project_col[i], satd_file_col[i], satd_and_td['code|design-debt'][i], satd_and_td['requirement-debt'][i], satd_and_td['documentation-debt'][i], satd_and_td['test-debt'][i], satd_and_td['total-debt'][i],
                            satd_and_td['TotalBrokenRules'][i], satd_and_td['Minor'][i], satd_and_td['Major'][i], satd_and_td['Critical'][i], satd_and_td['Info'][i], grime['cg-na'][index], grime['cg-npm'][index], grime['Pattern'][index], grime['count'][index]])
        else:
            writer.writerow([project_col[i], satd_file_col[i], satd_and_td['code|design-debt'][i], satd_and_td['requirement-debt'][i], satd_and_td['documentation-debt'][i], satd_and_td['test-debt'][i],
                            satd_and_td['total-debt'][i], satd_and_td['TotalBrokenRules'][i], satd_and_td['Minor'][i], satd_and_td['Major'][i], satd_and_td['Critical'][i], satd_and_td['Info'][i], 0, 0, 'None', 0])
