import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from queue import Queue
from tenacity import retry, stop_after_attempt, wait_exponential
import time
from scanner.logger import logger


# Liste indicative des noms de tokens CSRF
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}


# 3 tentatives de la fonction
@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=5))
def fetch_url(url):

    # requête HTTP GET vers l'URL spécifiée
    response = requests.get(url, timeout=5)
    #exception en cas d'erreur HTTP
    response.raise_for_status()
    return response

# formater l'url en une absolu en cas d'oubli
def format_url(url):
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url


# Fonction principale du crawling 
def crawl(start_url, max_pages=20, delay=0.5, verbose=False):
    # Initialisation
    # Ensemble pour suivre les sites déjà visitées
    visited_urls = set()
    # Deux files d'attente : haute et basse priorité
    high_priority_queue = Queue()
    low_priority_queue = Queue()
    # Liste des sites trouvées
    found_urls = []

    # Ajout de l'URL de départ dans les deux files
    high_priority_queue.put(start_url)
    low_priority_queue.put(start_url)

    crawl_count = 0  # initialisation du compteur du nombre de pages crawled

    # Jusqu'à ce qu'on atteigne MAX_CRAWL ou que les files soient vides
    while (not high_priority_queue.empty() or not low_priority_queue.empty()) and crawl_count < max_pages:
        # On prend la priorité haute en premier
        if not high_priority_queue.empty():
            current_url = high_priority_queue.get()
        else:
            current_url = low_priority_queue.get()

        # Ignore les urls déjà visités
        if current_url in visited_urls:
            continue

        visited_urls.add(current_url)

        try:
            # Récupération du contenu de la page
            response = fetch_url(current_url)        
            # transforme la réponse HTTP en un objet manipulable
            soup = BeautifulSoup(response.content, "html.parser")
            # Ajout du site aux sités trouvés
            found_urls.append(current_url)

            crawl_count += 1  

            if verbose:
                logger.info(f"Page crawlée : {current_url}")


            links = soup.find_all("a", href=True)
            for link in links:
                href = link["href"]
                absolute_url = urljoin(start_url, href)
                if absolute_url.startswith(start_url) and absolute_url not in visited_urls:
                    if "=" in absolute_url:  # On met les liens avec paramètres en priorité
                        high_priority_queue.put(absolute_url)
                    else:
                        low_priority_queue.put(absolute_url)


            time.sleep(delay)  # Pause entre les requêtes pour éviter de surcharger le serveur
        except requests.RequestException:
            if verbose:
                logger.warning(f"Échec d'accès à : {current_url}")
            continue

    return found_urls  # Retourne la liste des URLs collectées
