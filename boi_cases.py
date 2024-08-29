import re
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, ChunkedEncodingError, HTTPError



def boi_case2():
    # Case 2: <p class="paragraphe-western"> structure
    boi_section_p = soup.find('p', string=re.compile(r"Documents liés", re.IGNORECASE))
    if boi_section_p:
        for p in boi_section_p.find_next_siblings('p', class_='paragraphe-western'):
            link_element = p.find('a', href=True)
            if link_element:
                boi_code = link_element.text.strip()
                boi_href = link_element['href']
                description = p.get_text().replace(boi_code, '').strip(': ').strip()
                boi_files.append({
                    'code': boi_code, 
                    'link': boi_href,
                    'description': description
                })
    else:
        boi_case3()

def boi_case3():
    # Case 3: <div id="liste_docs_lies"> structure
    boi_liste_docs_lies = soup.find('div', id='liste_docs_lies')
    if boi_liste_docs_lies:
        for p in boi_liste_docs_lies.find_all('p', class_='paragraphe-western'):
            link_element = p.find('a', href=True)
            if link_element:
                boi_code = link_element.text.strip()
                boi_href = link_element['href']
                description = p.get_text().replace(boi_code, '').strip(': ').strip()
                boi_files.append({
                    'code': boi_code, 
                    'link': boi_href,
                    'description': description
                })
    else:
        boi_case4()

def boi_case4():
    # Case 4: <div class="content field--name-body" data-once="cookies-ajax"> structure
    boi_content_body = soup.find('div', class_='content field--name-body', attrs={'data-once': 'cookies-ajax'})
    if boi_content_body:
        for p in boi_content_body.find_all('p', id=re.compile(r'^.*_Documents_lies_:_.*$')):
            # Find paragraphs where the `id` contains "Documents_lies"
            if 'Documents liés' in p.get_text():
                continue
            link_element = p.find('a', href=True)
            if link_element:
                boi_code = link_element.text.strip()
                boi_href = link_element['href']
                description = p.get_text().replace(boi_code, '').strip(': ').strip()
                boi_files.append({
                    'code': boi_code, 
                    'link': boi_href,
                    'description': description
                })

