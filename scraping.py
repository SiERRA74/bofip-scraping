import requests
from bs4 import BeautifulSoup


for page in range(117):
    url = "https://bofip.impots.gouv.fr/actualites/toutes-les-actualites/all?page="
    url += str(page)

    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <a> tags with "TVA" in the title attribute and "ACTU" in href attribute
    actu_links = soup.find_all('a', href=lambda href: href and 'ACTU' in href)

    # Extract and print the href attribute of each <a> tag
    with open("data/links_bofip.txt", "a") as f:
        for link in actu_links:
            f.write("https://bofip.impots.gouv.fr" + link.get('href') + "\n")

