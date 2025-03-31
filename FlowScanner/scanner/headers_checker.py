# scanner/headers_checker.py

import requests


# Headers de sécurité recommandés
RECOMMENDED_HEADERS = {
    "Content-Security-Policy": "Protection contre les XSS",
    "Strict-Transport-Security": "Force HTTPS",
    "X-Content-Type-Options": "Empêche le MIME-sniffing",
    "X-Frame-Options": "Protection clickjacking",
    "X-XSS-Protection": "Ancienne protection XSS (obsolète)",
    "Referrer-Policy": "Contrôle les informations de referrer"
}

# Vérification des headers de sécurité
def check_security_headers(url):
    try:
        response = requests.get(url, timeout=5) # Requête HTTP GET
        headers = response.headers # Récupération des headers

        missing = {}
        for h in RECOMMENDED_HEADERS:
            if h not in headers:
                missing[h] = RECOMMENDED_HEADERS[h] # Si le header est manquant, ajout à la liste

        if missing:
            print(f"[Alerte] Headers de sécurité manquants sur {url} :")
            for h, desc in missing.items():
                print(f"    - {h} : {desc}") # Affichage des headers manquants

        return missing

    except requests.RequestException:
        print(f"Impossible d'accéder à {url}")
        return {}
