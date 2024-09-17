import xml.etree.ElementTree as ET
import os

# Define your filter array with the search terms
filter = ["code general des impôts", "livre des procédures fiscales"]
verified = 0  # Global variable to track how many files concern fiscalité


# Function to check if the file content contains fiscal keywords (or fuzzy match)
def verify_fisc(texte, filename, file_path):
    global verified  # Declare that we are using the global variable
    # Check if an exact match or fuzzy match exists
    for term in filter:
        # Direct (case-insensitive) match
        if term.lower() in texte.lower():
            print(f"\033[92m Le fichier '{filename}' CONCERNE la fiscalité \033[0m")
            verified += 1  # Increment the global verified count
            return True


    # If no match or fuzzy match is found, delete the file
    print(f"\033[91m Le fichier '{filename}' ne concerne PAS la fiscalité, suppression... \033[0m")
    os.remove(file_path)
    print(f"Fichier '{filename}' supprimé.")
    return False

# Directory to search for XML files
walk_dir = "C:/Users/aksie/Documents/fisca/..."

print('walk_dir = ' + walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

# Recursive walk through directories and files
for root_dir, subdirs, files in os.walk(walk_dir):
    for filename in files:
        # Only process XML files
        if filename.endswith('.xml'):
            file_path = os.path.join(root_dir, filename)

            print(f"\nProcessing file: {filename} (full path: {file_path})")

            try:
                # Parse the XML file
                tree = ET.parse(file_path)
                root = tree.getroot()

                # Collect all the text content from <p> tags
                text_all = ""
                for para in root.iter('p'):
                    if para.text:
                        text_all += para.text + "\n"

                # Verify if the content matches fiscal filter (or fuzzy match)
                verify_fisc(text_all, filename, file_path)

            except ET.ParseError as e:
                print(f"Error parsing file {filename}: {e}")
            except Exception as e:
                print(f"An error occurred while processing {filename}: {e}")

# After processing all files, print how many files concern fiscalité
print(f"\nTotal files that concern fiscalité: {verified}")

