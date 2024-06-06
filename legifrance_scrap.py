import json, os, requests, time
from bs4 import BeautifulSoup as soup
from info_harvestV2 import save_to_json

print("Changing legifrance links into text")


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
def run_link_harvest():
    print("Running main function")

# Call the run function
run_link_harvest()
