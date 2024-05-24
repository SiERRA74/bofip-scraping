import json, requests
import os
from bs4 import BeautifulSoup as soup

def html_request(link):
    response = requests.get(link)
    # Parse the HTML content with explicit UTF-8 encoding
    html_page = soup(response.content, 'html.parser', from_encoding='utf-8')
    return html_page

# Function to read the JSON file and return its content
def read_json(filename='data/bofip_test.json'):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} does not exist.")
    
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
    

# Function to iterate through each dictionary in the JSON file
def iterate_articles(data):
    for article_id, article_data in data['bofip'].items():
        process_article(article_id, article_data)



# Function to scrape content from each link
def scrape_link_content(article_id, soup, link):
   
    # Find the text and collect links
    text_elements = []

    for p in soup.find_all('p'):

        text_elements.append(p.get_text().strip())
    
    code_legifrance = ' '.join(text_elements)
    
    return code_legifrance


# Function to process each article
def process_article(article_id, article_data):
    code_legifrance = soup.find('div', class_='content')





# Main function to run the script
def run():
    data = read_json()  # Read the JSON file
    iterate_articles(data)  # Iterate and process each article

# Call the run function
run()
