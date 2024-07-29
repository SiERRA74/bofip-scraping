from bs4 import BeautifulSoup
import requests, time, re, json, os


bofip = {}

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

    text = ' '.join(text_elements)
    
    # Extract the link of the article itself
    article_link = link
    
    return article_id, {'title': title, 'division_serie': division_serie, 'text': text, 'link': article_link, 'legifrance': legifrance}


def remove_newlines(data):
    if isinstance(data, str):
        return data.replace('\n', ' ')
    elif isinstance(data, list):
        return [remove_newlines(item) for item in data]
    elif isinstance(data, dict):
        return {key: remove_newlines(value) for key, value in data.items()}
    return data


# Function to save scraped content to a file 
def save_to_json(data, filename='../bofip-scraping/data/bofip_data.json'):
    if not os.path.exists(filename):
        with open(filename, 'w+', encoding='utf-8') as f:
            json.dump({"bofip": {}}, f, indent=4, ensure_ascii=False)

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
    except json.JSONDecodeError:
        # Handle the case where the file is empty or contains invalid JSON
        json_data = {"bofip": {}}

    # Append the new data
    json_data['bofip'].update(data)

    # Save the updated data back to the JSON file
    with open(filename, 'w+', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

def run():
    with open("../bofip-scraping/data/actu_links.txt", "r", encoding="utf-8") as f:
        links = f.readlines()

    article_id = 1  # Initialize article ID counter

    for link in links:
        link = link.strip()
        html = html_request(link)
        article_id_str, article_data = scrape_link_content(article_id, html, link)
        article_data = remove_newlines(article_data)
        
        save_to_json({article_id_str: article_data})  # Save scraped content
        
        article_id += 1  # Increment article ID

    print("process : completed")

run()