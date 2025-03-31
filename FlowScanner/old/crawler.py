# pip3 install requests beautifulsoup4
import requests
import re
from bs4 import BeautifulSoup
import csv
from tenacity import retry, stop_after_attempt, wait_exponential
from queue import Queue
target_url = "https://www.scrapingcourse.com/ecommerce/"

url_pattern = re.compile(r"/page/\d+/")
product_data = []

# initialisation de la liste des découvertes urls
urls_to_visit = [target_url]

# Limite maximum de crawl
max_crawl = 20

session = requests.Session()

high_priority_queue = Queue()
low_priority_queue = Queue()
# create priority queues
high_priority_queue.put(target_url)
low_priority_queue.put(target_url)

# create a set to track visited URLs
visited_urls = set()

# implement a request retry
@retry(
    stop=stop_after_attempt(4),  # maximum number of retries
    wait=wait_exponential(multiplier=5, min=4, max=5),  # exponential backoff
)
def fetch_url(url):
    response = session.get(url)
    response.raise_for_status()
    return response

def crawler():
    # counter de crawl pour surveiller la profondeur de la recherche
    crawl_count = 0

    while (
        not high_priority_queue.empty() or not low_priority_queue.empty()
    ) and crawl_count < max_crawl:
        
        # update the priority queue
        if not high_priority_queue.empty():
            current_url = high_priority_queue.get()
        elif not low_priority_queue.empty():
            current_url = low_priority_queue.get()
        else:
           break

        if current_url in visited_urls:
            continue
                # add the current URL to the URL set
        visited_urls.add(current_url)

        # Requete http vers l'url du site
        response = fetch_url(current_url)
        # parser le HTML
        soup = BeautifulSoup(response.content, "html.parser")





        # On collecte les liens de l'url
        link_elements = soup.find_all("a", href=True)
        for link_element in link_elements:
            url = link_element["href"]

            # Conversion vers un chemin absolu d'url
            if not url.startswith("http"):
                absolute_url = requests.compat.urljoin(target_url, url)
            else:
                absolute_url = url

            # On s'assurer que le lien exploré correspond au domaine et qu'il n'a pas déjà été visité 
            if (
                absolute_url.startswith(target_url)
                and absolute_url not in visited_urls
            ):
                # prioritize product pages
                if url_pattern.search(absolute_url):
                    high_priority_queue.put(absolute_url)

                else:
                    low_priority_queue.put(absolute_url)

            
        #Si l'URL correspond au regex des pages alors on extrait 
        if url_pattern.search(current_url):
            # Recupére l'élément parents

            product_containers = soup.find_all("li", class_="product")

            # exflitrage des données des produits
            for product in product_containers:
                link_tag = product.find("a", class_="woocommerce-LoopProduct-link")
                image_tag = product.find("img")
                name_tag = product.find("h2", class_="product-name")
                price_tag = product.find("span", class_="price")
              
                if link_tag and image_tag and name_tag and price_tag:
              
                    data = {
                        "Url": product.find("a", class_="woocommerce-LoopProduct-link")[
                            "href"
                        ],
                        "Image": product.find("img", class_="product-image")["src"],
                        "Name": product.find("h2", class_="product-name").get_text(),
                        "Price": product.find("span", class_="price").get_text(),
                    }

                    # ajout des données dans les produits 
                    product_data.append(data)

            # maj du compteur d'exploration
            crawl_count += 1

    print(urls_to_visit) # Affichage

crawler()

# Stockage dans un fichier csv
csv_filename = "produits.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Url", "Image", "Name", "Price"])
    writer.writeheader()
    writer.writerows(product_data)