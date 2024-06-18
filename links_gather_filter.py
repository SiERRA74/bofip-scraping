import json
import os


# Function to read the JSON file and return its content
def read_json(filename='data/bofip_data.json'):
    print("Reading JSON")
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} does not exist.")
    
    with open(filename, 'r', encoding='utf-8') as f:
        print("JSON opened")
        return json.load(f)


# Function to read the existing links from the text file
def read_existing_links(filename='data/linked_articles.txt'):
    if not os.path.exists(filename):
        return set()  # Return an empty set if the file does not exist
    
    with open(filename, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)


# Function to save unique legifrance links to the text file
def save_to_file(unique_links, output_filename='data/linked_articles.txt'):
    with open(output_filename, 'a', encoding='utf-8') as f:
        for link in unique_links:
            f.write(link + "\n")


# Function to iterate through each dictionary in the JSON file and collect unique links
def iterate_articles(data, existing_links):
    print("Iterating articles begin")
    new_links = set()

    for article_id, article_data in data['bofip'].items():
        legifrance_links = article_data.get("legifrance", [])
        for link in legifrance_links:
            if link not in existing_links:
                new_links.add(link)
    
    return new_links


# Main function to run the script
def run():
    print("Running main function")
    data = read_json()  # Read the JSON file
    existing_links = read_existing_links()  # Read existing links from the text file
    new_links = iterate_articles(data, existing_links)  # Collect unique new links
    save_to_file(new_links)  # Save unique new links to the file


# Call the run function
run()
