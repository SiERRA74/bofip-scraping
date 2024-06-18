import re

def extract_hrefs_from_file(filename):
    hrefs = []
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        href_matches = re.findall(r'href="([^"]+)"', content)
        
        for href in href_matches:
            hrefs.append("https://bofip.impots.gouv.fr" + href)
    return hrefs

# Function to save links to a file
def save_links_to_file(links, filename):
    with open(filename, "w+", encoding='utf-8') as f:
        for link in links:
            f.write(link + '\n')

def run_boi_scrap():
    file_path = "data/plan_classement.txt"
    hrefs = extract_hrefs_from_file(file_path)
    save_links_to_file(hrefs, "data/BOI_links.txt")

run_boi_scrap()


"""
Serves to take all the available pages from https://bofip.impots.gouv.fr/plan-de-classement
You have to inspect that page, and to make sure to copy the right div : <div class="bofip_pdc treeview" style="height: auto;">
(after clicking "Tout déplier") 
And paste that HTML snippet to a file you have to name plan_classement.txt
"""