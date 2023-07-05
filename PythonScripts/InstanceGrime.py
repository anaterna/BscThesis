import csv
import xml.etree.ElementTree as ET

# Parse the XML file
tree = ET.parse('hbase_other.ssap.pttgrime.xml')
root = tree.getroot()


td_csv_file = 'CSV Files/merged.csv'

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
        satd_count = int(row['total-debt'])
        minor_count = int(float(row['Minor']))
        major_count = int(float(row['Major']))
        critical_count = int(float(row['Critical']))
        td_count_per_class[class_name] = {
            'TotalBrokenRules': td_count,
            'Minor': minor_count,
            'Major': major_count,
            'Critical': critical_count,
            'total-debt': satd_count
        }

for class_name in td_count_per_class:
    print(class_name, td_count_per_class[class_name])

# Assign instance IDs
instance_id = 1
for pattern in root.iter('pattern'):
    for instance in pattern.findall('instance'):
        instance.set('id', str(instance_id))
        instance_id += 1

# Create the CSV file
with open('instance_grime_jhotdraw.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Instance ID', 'Pattern', 'mg-ca', 'mg-ce', 'Number of Classes',
                    'Sum of cg-na', 'Sum of cg-npm', 'Sum of total-debt', 'TD', 'Minor', 'Major', 'Critical'])

    for pattern in root.iter('pattern'):
        pattern_name = pattern.get('name')

        for instance in pattern.findall('instance'):
            instance_id = instance.get('id')

            if instance.get('mg-ca') is None or instance.get('mg-ce') is None:
                continue

            mg_ca = instance.get('mg-ca')
            mg_ce = instance.get('mg-ce')

            classes = set()
            cg_na_sum = 0
            cg_npm_sum = 0
            satd_total = 0
            td_total = 0
            minor_total = 0
            major_total = 0
            critical_total = 0

            for role in instance.findall('role'):
                element = role.get('element')
                class_name = element.split('::')[0].split('$')[0]
                # print(class_name)

                if class_name not in classes:
                    package = extract_package(class_name)
                    # print(package)
                    # iterate through the td dictionary
                    for class_name2 in td_count_per_class:
                        if package in class_name2:
                            td_total += td_count_per_class[class_name2]['TotalBrokenRules']
                            minor_total += td_count_per_class[class_name2]['Minor']
                            major_total += td_count_per_class[class_name2]['Major']
                            critical_total += td_count_per_class[class_name2]['Critical']
                            satd_total += td_count_per_class[class_name2]['total-debt']
                            break

                classes.add(class_name)
                cg_na = 0
                cg_npm = 0

                if role.get('cg-na') is not None:
                    cg_na = role.get('cg-na')
                if role.get('cg-npm') is not None:
                    cg_npm = role.get('cg-npm')

                cg_na_sum += int(cg_na)
                cg_npm_sum += int(cg_npm)

            num_classes = len(classes)

            writer.writerow([instance_id, pattern_name, mg_ca, mg_ce, num_classes,
                            cg_na_sum, cg_npm_sum, satd_total, td_total, minor_total, major_total, critical_total])
