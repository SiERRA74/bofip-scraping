import json
import os
import requests
from bs4 import BeautifulSoup
import re

# Function to perform HTML request
def html_request(link):
    response = requests.get(link)
    # Parse the HTML content with explicit UTF-8 encoding
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
    return soup

# Function to scrape content from each link
def scrape_link_content(article_id, soup, link):
    article_id = f"article-{article_id}"
    # Extract the desired information
    title_element = soup.find('h1', class_='titre-news-du-document-western')
    title = title_element.text.strip() if title_element else "Title Not Found"
    
    # Find the division/serie
    division_serie_element = soup.find('p', string=re.compile(r"Série / Division", re.IGNORECASE))
    if division_serie_element:
        next_sibling = division_serie_element.find_next_sibling('p')
        division_serie = next_sibling.text.strip() if next_sibling else "Division/Serie Not Found"
    else:
        division_serie = "Division/Serie Not Found"
    
    # Find the text and collect links
    text_elements = []
    legifrance = []
    for p in soup.find_all('p'):
        if 'Actualité liée' in p.get_text():
            break
        text_elements.append(p.get_text().strip())
        
        # Find all links in the paragraph
        for a in p.find_all('a', href=True):
            if a['href'].startswith("https://www.legifrance.gouv.fr/"):
                legifrance.append(a['href'])
    
    text = ' '.join(text_elements)
    
    return article_id, title, division_serie, text, link, legifrance

# Function to remove newlines from data
def remove_newlines(data):
    if isinstance(data, str):
        return data.replace('\n', ' ')
    elif isinstance(data, list):
        return [remove_newlines(item) for item in data]
    elif isinstance(data, dict):
        return {key: remove_newlines(value) for key, value in data.items()}
    return data

# Function to save scraped content to a text file
def save_to_file(article_id, title, division_serie, text, link, legifrance, filename='data/bofip_data.txt'):
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("")

    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"-id {article_id}\n")
        f.write(f"- {title}\n")
        f.write(f"- {division_serie}\n")
        f.write(f"- {text}\n")
        f.write(f"- {link}\n")
        f.write(f"- {'\n '.join(legifrance)}\n")
        f.write("\n\n")

# Main function to run the script
def run_info_harvest():
    with open("data/links_bofip.txt", "r", encoding="utf-8") as f:
        links = f.readlines()

    article_id = 1  # Initialize article ID counter

    for link in links:
        link = link.strip()
        html = html_request(link)
        article_id_str, title, division_serie, text, link, legifrance = scrape_link_content(article_id, html, link)
        title, division_serie, text, link, legifrance = remove_newlines([title, division_serie, text, link, legifrance])
        
        save_to_file(article_id_str, title, division_serie, text, link, legifrance)  # Save scraped content
        
        article_id += 1  # Increment article ID

    print("Process completed")

run_info_harvest()
