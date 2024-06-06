import json, os, requests, time
from bs4 import BeautifulSoup as soup
from info_harvestV2 import save_to_json

print("Starting the correct script.")

# Function to read the JSON file and return its content
def read_json(filename='data/bofip_data.json'):
    print("Reading JSON")
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} does not exist.")
    
    with open(filename, 'r', encoding='utf-8') as f:
        print("JSON opened")
        return json.load(f)


# Function to iterate through each dictionary in the JSON file
def iterate_articles():
    global data
    print("Iterating articles begin")
    for article_id, article_data in data['bofip'].items():
        print(f"Iterating article {article_id}")
        legifrance_links = article_data["legifrance"]
        article_data["legifrance"] = process_links(legifrance_links)
        print(f"Updated {article_id} with legifrance content")
        save_to_json(data, "data/bofip_dataV2.json")
    print("Articles iteration complete")
 

# Function to process each legifrance link
def process_links(legifrance_links):
    processed_links = []
    for link in legifrance_links:
        page_soup = html_request(link)
        article_name, article_content = extract_content(page_soup)
        processed_links.append({
            "article_name": article_name,
            "article_content": article_content
        })
    return processed_links


def html_request(link):
    response = requests.get(link)
    # Parse the HTML content with explicit UTF-8 encoding
    html_page = soup(response.content, 'html.parser', from_encoding='utf-8')
    return html_page


def extract_content(page_soup):
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
        content_text = ""

    return article_name, content_text




# Main function to run the script
def run():
    print("Running main function")
    global data
    data = read_json()  # Read the JSON file
    iterate_articles()  # Iterate and process each article

# Call the run function
run()
