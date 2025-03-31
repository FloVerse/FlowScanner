# scanner/exposed_files.py

import requests

# Fichiers communs souvent exposés	
COMMON_FILES = [
    ".env",
    ".git/config",
    "wp-config.php",
    "config.php",
    "database.yml",
    "backup.zip",
    "dump.sql",
    "admin.bak",
    "index.php~"
]

# Vérifie si des fichiers communs sont exposés
def check_exposed_files(base_url):
    exposed = []

    if not base_url.endswith("/"):  # Ajout du / final si absent
        base_url += "/"

    for file in COMMON_FILES:
        test_url = base_url + file
        try:
            response = requests.get(test_url, timeout=5)
            if response.status_code == 200 and len(response.content) > 50: # Fichier trouvé
                exposed.append(test_url)
                print(f"[Alerte] Fichier exposé trouvé : {test_url}")
        except requests.RequestException:
            continue

    return exposed
