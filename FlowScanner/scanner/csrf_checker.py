# scanner/csrf_checker.py

import requests
from bs4 import BeautifulSoup

# Liste indicative des noms de tokens CSRF
TOKEN_NAMES = ["csrf", "token", "authenticity_token", "_csrf", "csrfmiddlewaretoken"]

# Vérifie si des formulaires POST ne contiennent pas de protection CSRF
def check_csrf_forms(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        forms = soup.find_all("form")

        potentially_vulnerable = []

        for form in forms:
            method = form.get("method", "get").lower()
            if method != "post":
                continue  # on ne vérifie que les formulaires POST

            inputs = form.find_all("input", attrs={"type": "hidden"})
            token_found = any(
                inp.get("name", "").lower() in TOKEN_NAMES for inp in inputs
            )

            if not token_found:
                potentially_vulnerable.append(str(form)[:300])  # extrait pour le rapport

        return potentially_vulnerable

    except requests.RequestException:
        return []
