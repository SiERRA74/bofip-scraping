import xml.etree.ElementTree as ET
import os
import json



# Function to process the XML files and extract the needed data
def extract_xml_data(file_path):
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract identification and date from Donnees_Techniques
        identification = ""
        date_mise_jour = ""

        donnees_techniques = root.find('Donnees_Techniques')
        if donnees_techniques is not None:
            identification = donnees_techniques.findtext('Identification', default="")
            date_mise_jour = donnees_techniques.findtext('Date_Mise_Jour', default="")

        # Extract the content from Texte_Integral under Decision
        content = ""
        decision = root.find('Decision')
        if decision is not None:
            texte_integral = decision.find('Texte_Integral')
            if texte_integral is not None:
                for para in texte_integral.iter('p'):
                    if para.text:
                        content += para.text + "  "

        # Extract metadata from Dossier
        metadata = {}
        dossier = root.find('Dossier')
        if dossier is not None:
            metadata = {
                "Code_Juridiction": dossier.findtext('Code_Juridiction', default=""),
                "Nom_Juridiction": dossier.findtext('Nom_Juridiction', default=""),
                "Numero_Dossier": dossier.findtext('Numero_Dossier', default=""),
                "Date_Lecture": dossier.findtext('Date_Lecture', default=""),
                "Avocat_Requerant": dossier.findtext('Avocat_Requerant', default=""),
                "Type_Decision": dossier.findtext('Type_Decision', default=""),
                "Type_Recours": dossier.findtext('Type_Recours', default=""),
                "Code_Publication": dossier.findtext('Code_Publication', default=""),
                "Solution": dossier.findtext('Solution', default="")
            }

        return identification, content.strip(), date_mise_jour, metadata

    except ET.ParseError as e:
        print(f"Error parsing file {file_path}: {e}")
        return None, None, None, None
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")
        return None, None, None, None

# Directory to search for XML files
xml_directory = "C:/Users/aksie/Documents/fisca/TA"   # <<<--- CHANGE HERE !!!

# Dictionary to hold all extracted data before saving to JSON
data_structure = {
    "Tribunaux administratifs": {}              # <<<--- CHANGE HERE !!!
}

# Recursive walk through directories and files
for root_dir, subdirs, files in os.walk(xml_directory):
    for filename in files:
        # Only process XML files
        if filename.endswith('.xml'):
            file_path = os.path.join(root_dir, filename)

            print(f"\nProcessing file: {filename} (full path: {file_path})")

            # Extract data from XML
            identification, content, date_mise_jour, metadata = extract_xml_data(file_path)
            
            if identification and content and date_mise_jour and metadata:
                # Add extracted data to the data structure
                document_data = {
                    "content": content,
                    "date": date_mise_jour,
                    "metadata": metadata
                }
                data_structure["Tribunaux administratifs"][filename] = document_data  # <<<--- CHANGE HERE !!!
            else:
                print(f"Skipping {filename} due to missing identification, content, date, or metadata")


# Ensure output directory exists
output_directory = "opendata"
os.makedirs(output_directory, exist_ok=True)

# Save the collected data to a JSON file
output_file = os.path.join(output_directory, "tribunaux_admin.json") # <<<--- CHANGE HERE !!!
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(data_structure, json_file, ensure_ascii=False, indent=4)

print(f"\nData extraction complete. JSON saved to {output_file}")
