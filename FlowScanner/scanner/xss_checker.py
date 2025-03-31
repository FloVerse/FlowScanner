# scanner/xss_checker.py

import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from bs4 import BeautifulSoup

XSS_PAYLOAD = "<script>alert('test')</script>"

# Injection du payload dans les paramètres GET
def inject_payload(url, payload):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    if not query:
        return None  # Pas de paramètres donc pas de test GET possible

    # Injecte le payload dans tous les paramètres
    injected_query = {k: payload for k in query}
    injected_query_string = urlencode(injected_query, doseq=True) # doseq=True pour gérer les listes de valeurs

    # Reconstruction de l'URL avec le payload
    injected_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        injected_query_string,
        parsed.fragment
    ))

    return injected_url


# Test de la vulnérabilité XSS
def test_xss(url):
    vulnerable = []
    test_url = inject_payload(url, XSS_PAYLOAD) # Injection du payload
    if not test_url:
        return vulnerable

    try:
        response = requests.get(test_url, timeout=5) # Requête GET
        if XSS_PAYLOAD in response.text: 
            vulnerable.append(test_url) # Si le payload est exécuté, vulnérabilité détectée
            print(f"[Alerte] Vulnérabilité XSS détectée sur : {test_url}") 
    except requests.RequestException:
        pass

    return vulnerable
