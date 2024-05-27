import json, os
from bs4 import BeautifulSoup as soup


# Function to read the JSON file and return its content
def read_json(filename='data/bofip_data.json'):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} does not exist.")
    
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
    


# Function to iterate through each dictionary in the JSON file
def iterate_articles(data):
    for article_id, article_data in data['bofip'].items():
        process_article(article_id, article_data)


# Function to process each article
def process_article(article_id, article_data):
    link = article_data['link']
    page_soup = html_request(link)
    # You can add more processing here if needed
    print(f"Processed {article_id}: {code_legifrance}")


def html_request(link):
    response = requests.get(link)
    # Parse the HTML content with explicit UTF-8 encoding
    html_page = soup(response.content, 'html.parser', from_encoding='utf-8')
    return html_page



# Main function to run the script
def run():
    data = read_json()  # Read the JSON file
    print(data["bofip"]["article-2"]["title"])
    #iterate_articles(data)  # Iterate and process each article

# Call the run function
run()
