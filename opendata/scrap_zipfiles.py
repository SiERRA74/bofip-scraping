import xml.etree.ElementTree as ET
import os

tree = ET.parse('opendata/DCA.xml')
root = tree.getroot()
content = root.attrib
text_all = ""

for para in root.iter('p'):
    text_all += (para.text+"\n")

print("\n==>>>L'INTEGRALITE du texte \n")
print(text_all)


def verify_fisc(texte):

    filter = ["code general des impôts","livre des procédures fiscales"]

    for i in range(len(filter)):
        if filter[i] in texte:
            return print("\033[92m Ce fichier CONCERNE la fiscalité \033[0m")
    print("\033[91m Ce fichier ne conerne PAS la fiscalité \033[0m")


verify_fisc(text_all)



"""file_path = 'opendata/DCA.xml'
file_size = os.path.getsize(file_path)
file_size_kb = file_size /1024  # Size in Kilobytes
print("File size {} Kb".format(file_size_kb))"""
