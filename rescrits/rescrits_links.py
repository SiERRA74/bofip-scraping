import requests
import os
from bs4 import BeautifulSoup

# Define the pages to scrape
pages = [
    "https://bofip.impots.gouv.fr/rescrits/division/413/Imp%C3%B4t%20sur%20le%20revenu",
    "https://bofip.impots.gouv.fr/rescrits/division/414/Revenus%20salariaux%20et%20assimil%C3%A9s",
    "https://bofip.impots.gouv.fr/rescrits/division/415/Revenus%20et%20profits%20du%20patrimoine%20mobilier",
    "https://bofip.impots.gouv.fr/rescrits/division/416/Revenus%20fonciers%20et%20profits%20du%20patrimoine%20immobilier",
    "https://bofip.impots.gouv.fr/rescrits/division/417/B%C3%A9n%C3%A9fices%20agricoles",
    "https://bofip.impots.gouv.fr/rescrits/division/418/B%C3%A9n%C3%A9fices%20non%20commerciaux",
    "https://bofip.impots.gouv.fr/rescrits/division/419/B%C3%A9n%C3%A9fices%20industriels%20et%20commerciaux",
    "https://bofip.impots.gouv.fr/rescrits/division/420/Imp%C3%B4ts%20sur%20les%20soci%C3%A9t%C3%A9s",
    "https://bofip.impots.gouv.fr/rescrits/division/421/Taxe%20sur%20la%20valeur%20ajout%C3%A9e",
    "https://bofip.impots.gouv.fr/rescrits/division/423/Cotisation%20sur%20la%20Valeur%20Ajout%C3%A9e%20des%20Entreprises",
    "https://bofip.impots.gouv.fr/rescrits/division/424/Taxes%20et%20participations%20sur%20les%20salaires",
    "https://bofip.impots.gouv.fr/rescrits/division/536/Impositions%20sur%20les%20%C3%A9nergies%2C%20les%20alcools%20et%20les%20tabacs",
    "https://bofip.impots.gouv.fr/rescrits/division/426/Imp%C3%B4ts%20fonciers",
    "https://bofip.impots.gouv.fr/rescrits/division/427/Imp%C3%B4ts%20sur%20le%20patrimoine",
    "https://bofip.impots.gouv.fr/rescrits/division/428/Enregistrement",
    "https://bofip.impots.gouv.fr/rescrits/division/434/S%C3%A9curit%C3%A9%20juridique"
]


def scrap_rescrits(page_array):
    all_links = []
    
    print("Processing links in pages...")
    
    for page in page_array:
        url = page
        response = requests.get(url)
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the div with id="itemsRescrits"
        items_rescrits_div = soup.find('div', id='itemsRescrits')
        
        # If the div is found, get all the <a> tags within it
        if items_rescrits_div:
            rescrit_links = items_rescrits_div.find_all('a')
            # Extract the href attributes and add them to the list
            for link in rescrit_links:
                href = link.get('href')
                if href:
                    # Complete the URL if it's relative
                    if not href.startswith('http'):
                        href = "https://bofip.impots.gouv.fr" + href
                    all_links.append(href)
    
    return all_links

def save_to_links(actu_links, filename="../bofip-scraping/rescrits/rescrits_links.txt"):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Save the links to the file
    with open(filename, "w+") as f:
        for link in actu_links:
            f.write(link + "\n")

def run_actu_links_scraping():
    data = scrap_rescrits(pages)
    save_to_links(data)
    print("All rescrit links scraping: completed")

# Call the run function
run_actu_links_scraping()

# Code made with Abdoul :D
