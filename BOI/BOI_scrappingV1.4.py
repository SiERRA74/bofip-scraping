import requests
from bs4 import BeautifulSoup
import json

# Function to send HTTP request and get the page content
def html_request(link):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            return BeautifulSoup(response.content, 'html.parser')
        else:
            print(f"Failed to fetch {link}. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request failed for {link}: {e}")
        return None

# Function to extract content from BOI and return title, text, and legifrance links
def extract_boi_content(page_soup):
    # Assuming the BOI page structure contains <title> and <div> for content
    title_element = page_soup.find('title')
    title = title_element.text.strip() if title_element else "Title Not Found"
    
    content_element = page_soup.find('div', class_='content')
    content_text = content_element.get_text(strip=True) if content_element else "Content Not Found"
    
    # Extract Legifrance links from the content
    legifrance_links = [a['href'] for a in page_soup.find_all('a', href=True) if 'legifrance' in a['href']]
    
    return title, content_text, legifrance_links

# Function to extract content from Legifrance pages
def extract_content_legifrance(page_soup):
    article_name = "Title Not Found"
    content_text = ""

    # Check for <article> or fallback to <div> as per Legifrance structure
    article_element = page_soup.find('article')
    if article_element:
        title_element = article_element.find(['h2', 'h4'])
        article_name = title_element.get_text(strip=True) if title_element else "Title Not Found"
        
        # Extract content paragraphs
        paragraphs = article_element.find_all('p')
        content_text = ' '.join(p.get_text(strip=True) for p in paragraphs)
    else:
        # If no article found, fallback to <div class="content-page">
        content_div = page_soup.find('div', class_='content-page')
        if content_div:
            title_element = content_div.find('h2', class_='title')
            article_name = title_element.get_text(strip=True) if title_element else "Title Not Found"
            content_divs = content_div.find_all('div')
            content_text = ' '.join(div.get_text(strip=True) for div in content_divs)

    return {
        "article_name": article_name,
        "content_text": content_text
    }

# Function to process Legifrance links
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

# Main function to scrape BOI documents and Legifrance articles, then save to JSON
def scrape_and_write_data(links_file, output_file):
    data = {"documents BOI": {}}  # Initializing the main dictionary as an empty dictionary
    with open(links_file, 'r', encoding='utf-8') as file:
        links = file.readlines()

    for idx, link in enumerate(links, start=1):
        link = link.strip()
        page_soup = html_request(link)  # Fetch BOI page content
        if page_soup:
            title, text, legifrance_links = extract_boi_content(page_soup)  # Extract BOI content

            if text:
                document_key = f"boifile-{idx}"  # Create a unique key for each document
                
                # Process Legifrance links to get article names and content
                processed_legifrance = process_links(legifrance_links)

                document_data = {
                    "link": link,
                    "title": title,  # Add title to the data
                    "text": text,
                    "legifrance": processed_legifrance  # Add processed legifrance links to the data
                }
                data["documents BOI"][document_key] = document_data  # Add each document under its unique key
                print(f"Scraped data from {link} and added to the dictionary as {document_key}")
            else:
                print(f"Failed to scrape content from {link}")
        else:
            print(f"Failed to load page for {link}")

    # Write the final data to the output JSON file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)
        print(f"Data written to {output_file}")

# Paths
links_file = "../bofip-scraping/BOI/BOI_links.txt"
output_file = "../bofip-scraping/BOI/BOI_dataV1.4.json"

# Run scraping and writing process
scrape_and_write_data(links_file, output_file)
