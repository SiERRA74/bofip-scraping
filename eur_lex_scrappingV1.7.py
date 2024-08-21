import re, requests, html


def extract_french_links(html_content):
    # Regular expression to match href attributes containing 'doclang=FR' but exclude those containing 'showPdf.jsf'
    french_links = re.findall(r'href="([^"]*doclang=FR[^"]*)"', html_content, re.IGNORECASE)
    french_text_links = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>.*?français.*?</a>', html_content, re.IGNORECASE)
    
    # Combine and remove duplicates
    all_french_links = list(set(french_links + french_text_links))
    
    # Filter out links containing 'showPdf.jsf'
    all_french_links = [link for link in all_french_links if 'showPdf.jsf' not in link]
    
    all_french_links = [html.unescape(link) for link in all_french_links]
    return all_french_links


def save_eurlex_links(french_links):
    links_list = [link + "\n" for link in french_links]

    with open("data/eurlex.txt", 'w+', encoding='utf-8') as f:
        f.writelines(links_list)


# Base URL and parameters
base_url = "https://curia.europa.eu/juris/documents.jsf"
params = {
    'nat': 'or',
    'mat': 'FISC%2Cor',
    'pcs': 'Oor',
    'jur': 'C,T,F',
    'dates': '%24type%3Dpro%24mode%3DfromTo%24from%3D2000.08.14%24to%3D2024.08.14',
    'language': 'fr',
    'cit': 'none%2CC%2CCJ%2CR%2C2008E%2C%2C%2C%2C%2C%2C%2C%2C%2C%2Ctrue%2Cfalse%2Cfalse',
    'td': '%24mode%3DfromTo%24from%3D2000.08.14%24to%3D2024.08.14%3B%3B%3BPUB1%3BNPUB1%3B%3B%3BORDALL',
    'avg': '',
    'lgrec': 'fr',
    'lg': ''
}

all_french_links = []

# Loop through pages
for page_num in range(1, 57):  # Adjust the range for the number of pages
    params['page'] = str(page_num)
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        html_content = response.text
        french_links = extract_french_links(html_content)
        all_french_links.extend(french_links)
    else:
        print(f"Failed to retrieve page {page_num}")

# Remove duplicates
all_french_links = list(set(all_french_links))

# Save the extracted French links to a file
save_eurlex_links(all_french_links)

print(f"Total links saved: {len(all_french_links)}")


