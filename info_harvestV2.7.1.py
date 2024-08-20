import re
import os
import json
from bs4 import BeautifulSoup
import requests
import time
from requests.exceptions import ConnectionError, ChunkedEncodingError, HTTPError

# Global variables to keep track of the counter and limit
counter = 0
limit = 1000  # Update the limit to 1000

# Function to process each legifrance link
def process_links(legifrance_links):
    processed_links = []
    for link in legifrance_links:
        page_soup = html_request(link)
        if page_soup:
            legifrance_content = extract_content_legifrance(page_soup)
            processed_links.append({
                "article_name": legifrance_content["article_name"],
                "article_link": link,
                "content_text": legifrance_content["content_text"]
            })
    return processed_links

# Function to extract content from legifrance pages
def extract_content_legifrance(page_soup):
    # Find the <article> element
    article_element = page_soup.find('article')
    if article_element:
        # Extract the title from the <h2> element within the <article>
        title_element = article_element.find('h2')
        article_name = title_element.text.strip() if title_element else "Title Not Found"
        
        # Extract all <p> elements within the <article>
        paragraphs = article_element.find_all('p')
        # Join the text content of each paragraph into a single string
        content_text = ' '.join(p.text.strip() for p in paragraphs)
    else:
        article_name = "Article Element Not Found"
        content_text = ""

    return {
        "article_name": article_name,
        "content_text": content_text
    }

# Function to make HTML requests with retries
def html_request(link, retries=5, backoff_factor=0.3):
    for i in range(retries):
        try:
            response = requests.get(link)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            # Parse the HTML content with explicit UTF-8 encoding
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
            return soup
        except (ConnectionError, ChunkedEncodingError, requests.exceptions.RequestException) as e:
            print(f"Attempt {i + 1} failed with error: {e}")
            if i < retries - 1:
                sleep_time = backoff_factor * (2 ** i)
                print(f"Retrying in {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
            else:
                print(f"Failed to fetch {link} after {retries} attempts.")
                return None
        except HTTPError as http_err:
            if response.status_code == 404:
                print(f"404 Error for {link}: {http_err}")
                return None  # Skip 404 errors
            else:
                print(f"HTTP error occurred for {link}: {http_err}")
                return None

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
    boi_section = soup.find('div', id='document-lies')

    if boi_section:
        boi_items = boi_section.find_all('p')
        for item in boi_items:
            link_element = item.find('a', href=True)
            if link_element:
                boi_code = link_element.text.strip()
                boi_href = link_element['href']
                # Get description by removing the code and link from the text
                boi_files.append({
                    'code': boi_code, 
                    'link': boi_href
                })

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
def save_to_json(data, filepath='../bofip-scraping/data/', base_filename='bofippp_data'):
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
        if html:  # Check if HTML request was successful
            try:
                article_id_str, article_data = scrape_link_content(article_id, html, link)
                article_data = remove_newlines(article_data)
                
                save_to_json({article_id_str: article_data})  # Save scraped content
                
                article_id += 1  # Increment article ID 
                counter += 1
            except Exception as e:
                print(f"Error processing {link}: {e}")
        else:
            print(f"Skipping {link} due to failed HTML request.")

    print("Process completed")

run()
