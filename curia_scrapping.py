import requests, json
from bs4 import BeautifulSoup


def scrap_curia():
    # Open the file containing the links
    with open("data/eurlex.txt", 'r', encoding='utf-8') as f:
        links = f.readlines()

    # Initialize an empty dictionary to store the results
    curia_data = {}

    # Process each link
    for link in links:
        link = link.strip()  # Remove any leading/trailing whitespace or newline characters

        # Send a GET request to the link
        response = requests.get(link)
        if response.status_code != 200:
            print(f"Failed to retrieve content from {link}")
            continue

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div with class "document_content"
        content_div = soup.find('div', class_='document_content')
        if content_div is None:
            print(f"No document content found for {link}")
            continue

        # Extract all paragraphs within the div
        paragraphs = content_div.find_all('p')

        # Ensure there are paragraphs in the div
        if not paragraphs:
            print(f"No paragraphs found in the document content for {link}")
            continue

        # The title is the first paragraph, and the rest are the content
        title = paragraphs[0].get_text(strip=True)
        content = "\n".join([p.get_text(strip=True) for p in paragraphs[1:]])

        # Store the scraped data in the dictionary
        curia_data[link] = {
            "title": title,
            "content": content
        }

    # Structure the data within a root "Curia" object
    curia_json = {"Curia": curia_data}

    # Save the result in a JSON file
    with open("data/curia_scraped.json", 'w+', encoding='utf-8') as json_file:
        json.dump(curia_json, json_file, indent=4, ensure_ascii=False)

    print(f"Scraping completed. Data saved in data/curia_scraped.json")

# Call the function to perform the scraping
scrap_curia()