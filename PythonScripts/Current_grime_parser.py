import xml.etree.ElementTree as ET
import csv
from collections import defaultdict

# This script is used to extract all the classes that have grime metrics based on the result of the spoon_pttgrime tool
# The output will contain classes that participate in unique and multiple instance of grime

# Parse the XML file
tree = ET.parse('./hbase_other.ssap.pttgrime.xml')
root = tree.getroot()

# Dictionary to store class details
class_dict = defaultdict(lambda: {'cg-na': 0, 'cg-npm': 0, 'pattern_names': set(), 'count':0})

# Iterate over pattern instances
for pattern in root.findall('pattern'):
    pattern_name = pattern.get('name')
    
    for instance in pattern.findall('instance'):
        instance_dict = defaultdict(lambda: {'cg-na': 0, 'cg-npm': 0})
        
        # Iterate over roles in each instance
        for role in instance.findall('role'):
            if role.get('cg-na') is not None:
                cg_na = int(role.get('cg-na', 0))
            else:
                continue
            
            cg_npm = int(role.get('cg-npm', 0))
            
            # Get class name from 'element' label
            element_text = role.get('element')
            class_name = element_text
            
            # Extract the class name
            if '::' in class_name:
                class_name = class_name.split('::')[0]
            
            if '$' in class_name:
                class_name = class_name.split('$')[0]
            

            # Update instance-level details
            instance_dict[class_name]['cg-na'] += cg_na
            instance_dict[class_name]['cg-npm'] += cg_npm
          
        # Update class details for the instance
        for class_name, class_details in instance_dict.items():
            class_dict[class_name]['cg-na'] += class_details['cg-na']
            class_dict[class_name]['cg-npm'] += class_details['cg-npm']
            class_dict[class_name]['pattern_names'].add(pattern_name)
            class_dict[class_name]['count'] += 1
            
           
            
# For classes in unique instance, get the entries where 'count' = 1
#class_dict = {class_name: class_details for class_name, class_details in class_dict.items() if class_details['count'] == 1}

# Example usage
with open('./FINAL_HB/all_grime_classes2.csv', 'w', newline='') as csvfile: 
    fieldnames = ['Class', 'cg-na', 'cg-npm', 'Pattern Name', 'count']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for class_name, class_details in class_dict.items():
        pattern_names = ';'.join(class_details['pattern_names'])
        writer.writerow({'Class': class_name, 'cg-na': class_details['cg-na'],
                         'cg-npm': class_details['cg-npm'], 'Pattern Name': pattern_names, 'count': class_details['count']})
