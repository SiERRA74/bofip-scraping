import requests
from bs4 import BeautifulSoup
import os
import threading
import time
from loading import loading  # Import the loading function from the spinner module

def scrap_news():
    for page in range(119):
        url = f"https://bofip.impots.gouv.fr/actualites/toutes-les-actualites/all?page={page}"
        response = requests.get(url)
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all <a> tags with "ACTU" in href attribute
        actu_links = soup.find_all('a', href=lambda href: href and 'ACTU' in href)
        
        # Yield each link found
        for link in actu_links:
            yield "https://bofip.impots.gouv.fr" + link.get('href')


def save_to_links(link, filename="data/links_bofip.txt"):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Append the link to the file
    with open(filename, "a") as f:
        f.write(link + "\n")

def run_actu_links_scraping():
    # Create a stop event for the spinner thread
    stop_event = threading.Event()
    # Start the loading spinner in a separate thread
    spinner_thread = threading.Thread(target=loading, args=(stop_event,), daemon=True)
    spinner_thread.start()
    
    try:
        for link in scrap_news():
            save_to_links(link)
    finally:
        stop_event.set()
        spinner_thread.join()  # Ensure the spinner thread has finished
    
    print("\nAll news links scraping: completed")

# Call the run function
run_actu_links_scraping()
