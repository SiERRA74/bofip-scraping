import requests, json, os, time
from bs4 import BeautifulSoup as bsoup

def scrap_curia_content(link, retries=3, backoff_factor=0.3):
    for attempt in range(retries):
        try:
            response = requests.get(link, timeout=10)
            response.raise_for_status()
            soup = bsoup(response.text, 'html.parser')

            content_div = soup.find('div', id='document_content')
            if content_div is None:
                print(f"No document content found for {link}")
                return None

            paragraphs = content_div.find_all('p')
            if not paragraphs:
                print(f"No paragraphs found in the document content for {link}")
                return None

            title = paragraphs[0].get_text(strip=True)
            content = "\n".join([p.get_text(strip=True) for p in paragraphs[1:]])

            return {
                "title": title,
                "content": content,
                "link": link
            }

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt + 1 < retries:
                sleep_time = backoff_factor * (2 ** attempt)
                print(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                print(f"Failed to retrieve content after {retries} attempts.")
                return None


def update_json(data, counter, filepath='../bofip-scraping/data/curia_scraped.json'):
    if not os.path.exists(filepath):
        with open(filepath, 'w+', encoding='utf-8') as f:
            json.dump({"Curia": {}}, f, indent=4, ensure_ascii=False)

    # Load existing data
    with open(filepath, 'r', encoding='utf-8') as f:
        existing_data = json.load(f)

    # Create a unique key using the counter
    key = f"curia-{counter}"
    
    # Update and saving the "Curia" section with new data
    existing_data['Curia'][key] = data
    with open(filepath, 'w+', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)

def main():
    # Open the file containing the links
    with open("data/eurlex.txt", 'r', encoding='utf-8') as f:
        links = f.readlines()

    # Process each link
    for counter, link in enumerate(links, start=1):
        link = link.strip() 
        scraped_data = scrap_curia_content(link)
        
        if scraped_data:
            update_json(scraped_data, counter)

    print(f"Scraping completed. Data saved in data/curia_scraped.json")


if __name__ == "__main__":
    main()
