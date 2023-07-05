import csv

# This script is used to merge the CSV files that contain the pattern details and grime instances 
# with the CSV file that contains the technical debt count per class
# The output contains classes that have TD and grime, only TD and only grime


# Take in the package of the class and output its subdirectory
def extract_package(class_name):
    package = class_name
    package = package.replace('.', '/')
    package += ".java"  # Append ".java" to the package name
    return package


def merge_csv_files(csv_file1, csv_file2, merged_csv_file):
    class_patterns = {}
    with open(csv_file2, 'r') as file2:
        reader2 = csv.DictReader(file2)
        for row in reader2:
            class_name = row['Class']
            class_package = extract_package(class_name)
            class_patterns[class_package] = {
                'Pattern': row['Pattern'],
                'cg-na': row['cg-na'],
                'cg-npm': row['cg-npm']
            }
    count_matches = 0
    with open(csv_file1, 'r') as file1, open(merged_csv_file, 'w', newline='') as merged_file:
        reader1 = csv.DictReader(file1)
        fieldnames = reader1.fieldnames
        fieldnames.extend(['Pattern', 'cg-na', 'cg-npm'])
        writer = csv.DictWriter(merged_file, fieldnames=fieldnames)
        writer.writeheader()

        matched_classes = set()
        for row in reader1:
            class_name = row['Class']
            matched = False
            for class_package, class_info in class_patterns.items():
                if class_package in class_name:
                    row['Pattern'] = class_info['Pattern']
                    row['cg-na'] = class_info['cg-na']
                    row['cg-npm'] = class_info['cg-npm']
                    writer.writerow(row)
                    matched = True
                    matched_classes.add(class_package)
                    count_matches+=1
                    print(class_package)
                    break
            # Remove this part if you want to exclude classes that have no grime 
            if not matched:
                row['Pattern'] = 'NONE'
                row['cg-na'] = 0
                row['cg-npm'] = 0
                writer.writerow(row)

        # Remove this part if you want to exclude classes that have no TD
        for class_package, class_info in class_patterns.items():
            if class_package not in [row['Class'] for row in reader1] and class_package not in matched_classes:
                empty_row = {fieldname: '0' for fieldname in fieldnames}
                empty_row['Class'] = class_package
                empty_row['Pattern'] = class_info['Pattern']
                empty_row['cg-na'] = class_info['cg-na']
                empty_row['cg-npm'] = class_info['cg-npm']
                # print(empty_row)
                writer.writerow(empty_row)


# Example usage
merge_csv_files('./csv_files_hbase/aggregated_TD.csv', './FINAL_HB/all_grime_classes.csv', './FINAL_HB/all_merged_files.csv')

# Remove a colomn in a CSV file
def remove_column(csv_file, column_index):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Remove the specified column from each row
    for row in rows:
        del row[column_index]

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

# Example usage
# remove_column('./unique_merged_files.csv', 5)  # Remove the 3rd column (index 2)