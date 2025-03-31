# scanner/directory_listing.py

import requests
from urllib.parse import urljoin

# Répertoires communs souvent exposés
COMMON_DIRECTORIES = [
    "uploads/",
    "images/",
    "files/",
    "documents/",
    "backup/",
    "logs/",
    "export/",
    "private/"
]


# Vérifie si des répertoires communs sont exposés
def check_directory_listing(base_url):
    vulnerable_dirs = []

    if not base_url.endswith("/"):
        base_url += "/"

    for directory in COMMON_DIRECTORIES:
        test_url = urljoin(base_url, directory)
        try:
            response = requests.get(test_url, timeout=5)
            content = response.text.lower()
            if ( response.status_code == 200 and ("index of /" in content or "<title>index of" in content) ):
                vulnerable_dirs.append(test_url)
                print(f"[Alerte] Directory listing détecté sur : {test_url}")
        except requests.RequestException:
            continue

    return vulnerable_dirs
