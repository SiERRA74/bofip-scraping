import re
import os
import json
from bs4 import BeautifulSoup
import requests

# Global variables to keep track of the counter and limit
counter = 0
limit = 1000  # Update the limit to 1000

# Function to process each legifrance link
def process_links(legifrance_links):
    processed_links = []
    for link in legifrance_links:
        page_soup = html_request(link)
        article_name = extract_content_legifrance(page_soup)
        processed_links.append({
            "article_name": article_name,
            "article_link": link
        })
    return processed_links

# Function to extract content from legifrance pages
def extract_content_legifrance(page_soup):
    # Extract the article name
    article_name_element = page_soup.find(['p', 'h2'], class_='name-article')
    if article_name_element:
        # If the article name is within a <span> tag, get the text from the <span>
        span_element = article_name_element.find('span')
        article_name = span_element.text.strip() if span_element else article_name_element.text.strip()
    else:
        article_name = "Article Name Not Found"

    # Extract the content
    content_div = page_soup.find('div', attrs={'data-a': 'false'})
    if content_div:
        content_paragraphs = content_div.find_all('p')
        # Filter out irrelevant paragraphs
        content_text = ' '.join(p.text.strip() for p in content_paragraphs if p.get('id') != 'label-recherche')
    else:
        # Try to find content within other potential divs if the first search fails
        content_div_alternate = page_soup.find('div', class_='content')
        if content_div_alternate:
            content_paragraphs = content_div_alternate.find_all('p')
            content_text = ' '.join(p.text.strip() for p in content_paragraphs if p.get('id') != 'label-recherche')
        else:
            content_text = ""
    return article_name

# Function to make HTML requests
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
        next_p_element = division_serie_element.find_next_sibling('p')
        division_serie = next_p_element.text.strip() if next_p_element else "Division/Serie Not Found"
    else:
        division_serie = "Division/Serie Not Found"
    
    # Find the text and collect links
    text_elements = []
    legifrance = []
    boi_files = []

    # Iterate through all <p> tags and <blockquote> tags
    for container in soup.find_all(['p', 'blockquote']):
        if container.name == 'blockquote':
            paragraphs = container.find_all('p')
        else:
            paragraphs = [container]
        
        for p in paragraphs:
            if 'Actualité liée' in p.get_text():
                break
            text_elements.append(p.get_text().strip())
            
            # Find all links in the paragraph
            for a in p.find_all('a', href=True):
                if a['href'].startswith("https://www.legifrance.gouv.fr/"):
                    legifrance.append(a['href'])
    

# Updated section to find BOI files in "Documents liés :"
    boi_sections = soup.find_all('div', class_='document-lies') + soup.find_all('div', id='document-lies') + soup.find_all('div', class_='content field--name-body')

    for boi_section in boi_sections:
        if boi_section:
            boi_items = boi_section.find_all('p', class_=['paragraphe-western', 'paragraphe-rescrit-actu-western'])
            for item in boi_items:
                link_element = item.find('a', href=True)
                if link_element:
                    boi_code = link_element.text.strip()
                    boi_desc = item.get_text().replace(boi_code, '').strip(' :')
                    if boi_code and boi_desc:
                        boi_files.append({'code': boi_code, 'description': boi_desc})

    text = ' '.join(text_elements)
    
    # Extract the link of the article itself
    article_link = link
    
    # Process Legifrance links
    processed_legifrance_links = process_links(legifrance)
    
    return article_id, {
        'title': title, 
        'division_serie': division_serie, 
        'text': text, 
        'link': article_link, 
        'legifrance': processed_legifrance_links,
        'boi_files': boi_files
    }

def remove_newlines(data):
    if isinstance(data, str):
        return data.replace('\n', ' ')
    elif isinstance(data, list):
        return [remove_newlines(item) for item in data]
    elif isinstance(data, dict):
        return {key: remove_newlines(value) for key, value in data.items()}
    return data

# Function to save scraped content to a file 
def save_to_json(data, filepath='../bofip-scraping/data/', base_filename='bofip_data'):
    global counter, limit
    current_partition = (counter // limit) * limit
    next_partition = current_partition + limit
    filename = f'{base_filename}_{current_partition}_{next_partition}.json'

    full_path = os.path.join(filepath, filename)

    if not os.path.exists(full_path):
        with open(full_path, 'w+', encoding='utf-8') as f:
            json.dump({"bofip": {}}, f, indent=4, ensure_ascii=False)

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
    except json.JSONDecodeError:
        # Handle the case where the file is empty or contains invalid JSON
        json_data = {"bofip": {}}

    # Append the new data
    json_data['bofip'].update(data)

    # Save the updated data back to the JSON file
    with open(full_path, 'w+', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

def run():
    global counter
    with open("data/actu_links.txt", "r", encoding="utf-8") as f:
        links = f.readlines()

    article_id = 1  # Initialize article ID counter

    for link in links:
        link = link.strip()
        html = html_request(link)
        article_id_str, article_data = scrape_link_content(article_id, html, link)
        article_data = remove_newlines(article_data)
        
        save_to_json({article_id_str: article_data})  # Save scraped content
        
        article_id += 1  # Increment article ID 
        counter += 1

    print("Process completed")

run()
