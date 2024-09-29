import requests
from bs4 import BeautifulSoup
import json

def html_request(link):
    response = requests.get(link)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"Failed to fetch {link}. Status code: {response.status_code}")
        return None

def scrape_text_and_legifrance_links(link):
    soup = html_request(link)
    if soup:
        # Extract the title (h1)
        title_element = soup.find('h1')
        title = title_element.get_text(strip=True) if title_element else "Title Not Found"
        
        # Extract the text from paragraphs with the class 'paragraphe-western'
        paragraphs = soup.find_all('p', class_='paragraphe-western')
        text = '  '.join(p.get_text(strip=True).replace('\n', '  ') for p in paragraphs)  # Replace \n with double spaces
        
        # Extract only links containing 'https://www.legifrance.gouv.fr/codes/' and exclude 'circulaires'
        legifrance_links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if 'https://www.legifrance.gouv.fr/codes/' in href:  # Only take specific 'codes' links
                legifrance_links.append(href)

        return title, text, legifrance_links
    else:
        return None, None, None

def scrape_and_write_data(links_file, output_file):
    data = {"documents BOI": {}}  # Initializing the main dictionary as an empty dictionary
    with open(links_file, 'r', encoding='utf-8') as file:
        links = file.readlines()

    for idx, link in enumerate(links, start=1):
        link = link.strip()
        title, text, legifrance_links = scrape_text_and_legifrance_links(link)
        
        if text:
            document_key = f"boifile-{idx}"  # Create a unique key for each document
            document_data = {
                "link": link,
                "title": title,  # Add title to the data
                "text": text,
                "legifrance": legifrance_links  # Add legifrance links to the data
            }
            data["documents BOI"][document_key] = document_data  # Add each document under its unique key
            print(f"Scraped data from {link} and added to the dictionary as {document_key}")
        else:
            print(f"Failed to scrape data from {link}")

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)
        print(f"Data written to {output_file}")

# Paths
links_file = "../bofip-scraping/BOI/BOI_links.txt"
output_file = "../bofip-scraping/BOI/BOI_data.json"

# Run scraping and writing process
scrape_and_write_data(links_file, output_file)
