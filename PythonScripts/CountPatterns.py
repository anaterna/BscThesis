import csv
from xml.etree import ElementTree as ET
from collections import defaultdict
import matplotlib.pyplot as plt

# Count the number of classes for each pattern
def count_pattern_classes(input_file, output_file):
    # Load XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Extract pattern instances and their classes
    pattern_classes = defaultdict(set)
    for pattern_node in root.findall(".//pattern"):
        pattern_name = pattern_node.attrib.get("name")
        for instance_node in pattern_node.findall(".//instance"):
            for role_node in instance_node.findall(".//role"):
                element = role_node.attrib.get("element")
                class_name = get_class_name(element)
                if class_name:
                    pattern_classes[pattern_name].add(class_name)

    # Find patterns with no instances
    all_patterns = set(pattern_node.attrib.get("name") for pattern_node in root.findall(".//pattern"))
    patterns_with_instances = set(pattern_classes.keys())
    patterns_without_instances = all_patterns - patterns_with_instances

    # Initialize counts for patterns without instances
    for pattern_name in patterns_without_instances:
        pattern_classes[pattern_name] = set()

    # Compute total class counts for each pattern
    pattern_class_counts = []
    for pattern_name, classes in pattern_classes.items():
        class_count = len(classes)
        pattern_class_counts.append((pattern_name, class_count))

    # Write results to CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Pattern', 'ClassCount'])
        writer.writerows(pattern_class_counts)

    print(f"Pattern class counts successfully written to {output_file}")

# Extract the class name from an element 
def get_class_name(element):
    parts = element.split("::")
    class_name = parts[0].split(":")[0] if len(parts) > 1 else parts[0]
    return class_name.strip()


# Plot the pattern class counts
def plot_pattern_classes(csv_file):
    patterns = []
    class_counts = []

    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        sorted_rows = sorted(reader, key=lambda row: int(row['ClassCount']), reverse=False)
        for row in sorted_rows:
            patterns.append(row['Pattern'])
            class_counts.append(int(row['ClassCount']))

    plt.barh(patterns, class_counts)
    plt.xlabel('Class Count')
    plt.ylabel('Pattern')
    plt.title('Pattern Class Counts')
    plt.tight_layout()  # Add this line to prevent cropping of titles
    # Save the figure (optional)
    plt.savefig(f'charts/pattern_distribution.png')

    plt.show()

# Usage example
input_file = '././ssap/patterns.ssap.xml'
output_file = 'output.csv'

# Generate the CSV file with pattern class counts
count_pattern_classes(input_file, output_file)

# Plot the results
plot_pattern_classes(output_file)