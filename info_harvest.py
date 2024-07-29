import requests
from bs4 import BeautifulSoup
import time
import re

# Function to scrape content from each link
def scrape_link_content(link, article_id):
    response = requests.get(link)
    
    # Parse the HTML content with explicit UTF-8 encoding
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
    
    # Extract the desired information
    title_element = soup.find('h1', class_='titre-news-du-document-western')
    title = title_element.text.strip() if title_element else "Title Not Found"
    
    # Find the division/serie
    division_serie_element = soup.find('p', string=re.compile(r"Série / Division", re.IGNORECASE))
    division_serie = division_serie_element.find_next_sibling('p').text.strip() if division_serie_element else "Division/Serie Not Found"
    
    # Find the text
    text_element = soup.find('p', string=re.compile(r"Texte", re.IGNORECASE))
    text = text_element.find_next_sibling('p').text.strip() if text_element else "Text Not Found"
    
    # Extract the link of the article itself
    article_link = link
    
    return article_id, title, division_serie, text, article_link

# Function to save scraped content to a file
def save_to_file(article_id, title, division_serie, text, article_link):
    with open("data/scraped_content.txt", "a", encoding="utf-8") as f:
        f.write("id_article: " + str(article_id) + "\n")
        f.write("titre: " + title + "\n")
        f.write("division " + division_serie + "\n")
        f.write("text: " + text + "\n")
        f.write("linked_article " + article_link + "\n\n")



with open("../bofip-scraping/data/actu_links.txt", "r", encoding="utf-8") as f:
    links = f.readlines()

article_id = 1  # Initialize article ID counter


for link in links:
    link = link.strip()

    article_id, title, division_serie, text, article_link = scrape_link_content(link, article_id)
    
    save_to_file(article_id, title, division_serie, text, article_link) # Save scraped content
    
    article_id += 1  # Increment article ID
    
    time.sleep(1)  # Delay



"""

Imports de bibliothéque pythons

Définition des fonctions extract_links() et write_links_to_file()

Open file, ouverture du fichier links_bofip.txt
Récupération des liens avec f.readlines()

Boucle passant à travers tous les liens. 
    – À chaque itération, link.strip()
    – appel de la fonction scrap_link_content() qui prend toutes les informations utiles
    – appel de la fonciton save_to_file()
    – incrémentation de article_id qui permet de garder trace du nombre d'itérations
    — time.sleep(1) : délai avant la prochaine itération.


scrap_link_content() : récupération des différents paragraphes utiles au programme
save_to_file() : récupération d' article_id, title, division_serie, text, article_link
et écriture de ces informations dans le fichier scraped_content.txt

"""