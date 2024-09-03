import xml.etree.ElementTree as ET
import os

tree = ET.parse('opendata/country.xml')
root = tree.getroot()
content = root.attrib

for country in root.findall('country'):
    # using root.findall() to avoid removal during traversal
    rank = int(country.find('rank').text)
    if rank > 50:
        root.remove(country)


tree.write('opendata/country.xml')


"""file_path = 'opendata/DCA.xml'
file_size = os.path.getsize(file_path)
file_size_kb = file_size /1024  # Size in Kilobytes
print("File size {} Kb".format(file_size_kb))"""
