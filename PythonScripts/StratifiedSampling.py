import csv
import random

# Generate a validation dataset based on stratified sampling
# input_file - the input CSV file
# output_file - the output CSV file
# sample_size - the number of samples to be generated
# stratify_field - the field to be used for stratification
# The methods devides the input dataset into groups based on the stratify field
# and then performs random sampling on each group
# The output CSV file contains the sampled data of the randomly selected groups
def stratified_sampling(input_file, output_file, sample_size, stratify_field):
    # Read the input CSV file
    data = []
    with open(input_file, 'r') as file:
        reader = csv.DictReader(file)
        header = reader.fieldnames
        for row in reader:
            data.append(row)

    # Group the data by the stratify field (patterns)
    groups = {}
    for row in data:
        patterns = row[stratify_field].split(', ')
        for pattern in patterns:
            if pattern not in groups:
                groups[pattern] = []
            groups[pattern].append(row)

    # Remove patterns with no associated classes
    groups = {pattern: rows for pattern, rows in groups.items() if rows}

    # Determine sample size per pattern group
    num_patterns = len(groups)
    sample_size_per_group = sample_size // num_patterns

    # Perform stratified sampling
    sampled_data = []
    for pattern, rows in groups.items():
        if len(rows) <= sample_size_per_group:
            sampled_data.extend(rows)
        else:
            sampled_data.extend(random.sample(rows, sample_size_per_group))

    # Write the sampled data to the output CSV file
    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(sampled_data)

        
# Example usage
input_file = './stratified_sampling.csv'
output_file = 'stratified_sampling_grime_karol.csv'
sample_size = 148 # 20 % population proportion 
stratify_field = 'Pattern'

stratified_sampling(input_file, output_file, sample_size, stratify_field)
