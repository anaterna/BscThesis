import csv
import xml.etree.ElementTree as ET

# Path to the XML file
xml_file = 'hbase_other.ssap.pttgrime.xml'

# Create a list to store the pattern details
pattern_list = []

# Parse the XML file
tree = ET.parse(xml_file)
root = tree.getroot()


td_csv_file = './CSV Files/merged.csv'

# Create a dictionary to store the technical debt count per class
td_count_per_class = {}


def extract_package(class_name):
    package = class_name
    # package = package.replace('.', '/')
    package += ".java"  # Append ".java" to the package name
    return package


# Read the technical debt CSV file and populate the td_count_per_class dictionary
with open(td_csv_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['project'] != 'hbase':
            continue
        class_name = row['file']
        td_count = int(row['TotalBrokenRules'])
        total_satd = int(float(row['total-debt']))
        minor_count = int(float(row['Minor']))
        major_count = int(float(row['Major']))
        critical_count = int(float(row['Critical']))
        td_count_per_class[class_name] = {
            'TotalBrokenRules': td_count,
            'Minor': minor_count,
            'Major': major_count,
            'Critical': critical_count,
            'total-debt': total_satd
        }


# Iterate over each pattern element
for pattern in root.findall('pattern'):
    pattern_name = pattern.get('name')
    instances = pattern.findall('instance')

    # Initialize variables for pattern-level aggregation
    mg_ca_total = 0
    mg_ce_total = 0
    cg_na_total = 0
    cg_npm_total = 0
    td_total = 0
    satd_total = 0
    minor_total = 0
    major_total = 0
    critical_total = 0
    class_set = set()

    # Iterate over each instance within the pattern
    for instance in instances:
        if instance.get('mg-ca') is None:
            continue

        mg_ca = int(instance.get('mg-ca'))
        mg_ce = int(instance.get('mg-ce'))

        # Iterate over each role within the instance
        for role in instance.findall('role'):
            if role.get('cg-na') is not None:
                cg_na = int(role.get('cg-na'))
            else:
                cg_na = 0
            if role.get('cg-npm') is not None:
                cg_npm = int(role.get('cg-npm'))
            else:
                cg_npm = 0
            element = role.get('element')
            class_name = element.split('::')[0].split('$')[0]

            if class_name not in class_set:
                package = extract_package(class_name)
                # iterate through the td dictionary
                for class_name2 in td_count_per_class:
                    # print(package, class_name2)
                    if package in class_name2:
                        td_total += td_count_per_class[class_name2]['TotalBrokenRules']
                        minor_total += td_count_per_class[class_name2]['Minor']
                        major_total += td_count_per_class[class_name2]['Major']
                        critical_total += td_count_per_class[class_name2]['Critical']
                        satd_total += td_count_per_class[class_name2]['total-debt']
                        break

            class_set.add(class_name)

            # Sum up the variables for pattern-level aggregation
            cg_na_total += cg_na
            cg_npm_total += cg_npm

        # Sum up the variables for pattern-level aggregation
        mg_ca_total += mg_ca
        mg_ce_total += mg_ce

    # Create a dictionary for pattern details
    pattern_details = {
        'Pattern': pattern_name,
        'mg-ca': mg_ca_total,
        'mg-ce': mg_ce_total,
        'cg-na': cg_na_total,
        'cg-npm': cg_npm_total,
        'TotalBrokenRules': td_total,
        'Minor': minor_total,
        'Major': major_total,
        'Critical': critical_total,
        'Instance Count': len(instances),
        'Class Count': len(class_set),
        'SATD': satd_total
    }

    # Append pattern details to the list
    pattern_list.append(pattern_details)

# Specify the output CSV file path
output_csv = 'pattern_grime.csv'

# Write the pattern details to the CSV file
fieldnames = ['Pattern', 'mg-ca', 'mg-ce', 'cg-na', 'cg-npm', 'TotalBrokenRules',
              'Minor', 'Major', 'Critical', 'Instance Count', 'Class Count', 'SATD']
with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(pattern_list)

print("CSV file generated successfully!")
