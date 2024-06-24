import requests
from bs4 import BeautifulSoup

def html_request(link):
    response = requests.get(link)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"Failed to fetch {link}. Status code: {response.status_code}")
        return None

def scrape_text_from_link(link):
    soup = html_request(link)
    if soup:
        paragraphs = soup.find_all('p', class_='paragraphe-western')
        text = ' '.join(p.get_text(strip=True) for p in paragraphs)
        return text
    else:
        return None

def scrape_and_write_data(links_file, output_file):
    with open(links_file, 'r', encoding='utf-8') as file:
        links = file.readlines()

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for idx, link in enumerate(links, start=1):
            link = link.strip()
            text = scrape_text_from_link(link)
            if text:
                outfile.write(text + '\n\n')
                print(f"Scraped data from {link} and wrote to {output_file}")
            else:
                print(f"Failed to scrape data from {link}")

# Paths
links_file = "data/BOI_links.txt"
output_file = "data/BOI_data.txt"

# Run scraping and writing process
scrape_and_write_data(links_file, output_file)

"""This code reads BOI URLs from a plan_classement.txt, scrapes text content from each URL, and writes the scraped data to an output file : BOI_data.txt."""