import re, os, json, requests, time, textwrap
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, ChunkedEncodingError, HTTPError

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

# Function to scrape the content of the <article> tag with id="article"
def scrape_rescrits_content(soup, wrap_width=80):
    rescrit_data = {}

    # Extract the title from the <h1> tag
    title = soup.find('h1')
    if title:
        rescrit_data['title'] = title.get_text(strip=True)
    else:
        rescrit_data['title'] = "No title found"

    # Extract the content from the <article> tag
    article = soup.find('article', id='article')
    if article:
        paragraphs = article.find_all('p')
        article_text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        
        # Wrap the text to improve readability
        wrapped_text = textwrap.fill(article_text, width=wrap_width)
        
        rescrit_data['content'] = wrapped_text
    else:
        rescrit_data['content'] = "No <article> tag with id='article' found."

    return rescrit_data

# Function to save scraped content to a file
def save_to_json(data, filepath='../bofip-scraping/rescrits/', limit=1000):
    global rescrits_counter

    full_path = os.path.join(filepath, 'rescrits.json')

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    if not os.path.exists(full_path):
        with open(full_path, 'w+', encoding='utf-8') as f:
            json.dump({"rescrits": {}}, f, indent=4, ensure_ascii=False)

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
    except json.JSONDecodeError:
        # Handle the case where the file is empty or contains invalid JSON
        json_data = {"rescrits": {}}

    # Append the new data
    json_data['rescrits'].update(data)

    # Save the updated data back to the JSON file
    with open(full_path, 'w+', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

def run():
    global rescrits_counter
    with open("rescrits/rescrits_links.txt", "r", encoding="utf-8") as f:
        links = f.readlines()

    rescrit_id = 1  # Initialize article ID counter

    for link in links:
        link = link.strip()
        soup = html_request(link)
        if soup:  # Check if HTML request was successful
            try:
                rescrit_data = scrape_rescrits_content(soup)
                rescrit_id_str = f'rescrit_{rescrit_id}'
                
                save_to_json({rescrit_id_str: rescrit_data})  # Save scraped content
                
                rescrit_id += 1  # Increment article ID 
                rescrits_counter += 1
            except Exception as e:
                print(f"Error processing {link}: {e}")
        else:
            print(f"Skipping {link} due to failed HTML request.")

    print("Process completed")

# Global counter initialization
rescrits_counter = 0

# Start the process
run()
