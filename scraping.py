import requests
from bs4 import BeautifulSoup
import os

def scrap_news():
    all_links = []
    print("processing links in pages")
    for page in range(122):
        url = f"https://bofip.impots.gouv.fr/actualites/toutes-les-actualites/all?page={page}"
        response = requests.get(url)
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all <a> tags with "ACTU" in href attribute
        actu_links = soup.find_all('a', href=lambda href: href and 'ACTU' in href)
        all_links.extend(actu_links)
    return all_links

def save_to_links(actu_links, filename="../bofip-scraping/data/actu_links.txt"):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    
    # Extract and print the href attribute of each <a> tag
    with open(filename, "w+") as f:
        for link in actu_links:
            f.write("https://bofip.impots.gouv.fr" + link.get('href') + "\n")

def run_actu_links_scraping():
    data = scrap_news()
    save_to_links(data)
    print("All news links scraping: completed")

# Call the run function
run_actu_links_scraping()

#Code made with Abdoul :D