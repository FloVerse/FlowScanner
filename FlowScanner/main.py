# main.py

from scanner.crawler import crawl, format_url
from scanner.sql_injection import test_sql_injection
from scanner.xss_checker import test_xss
from scanner.headers_checker import check_security_headers
from report.generator import generate_html_report
from scanner.exposed_files import check_exposed_files
from scanner.directory_listing import check_directory_listing
from scanner.csrf_checker import check_csrf_forms
from scanner.logger import logger

import re

#Vérification de l'URL
def is_valid_url(url):
    pattern = re.compile(r"^https?://[^\s/$.?#].[^\s]*$")
    return bool(pattern.match(url))

#Scanne une page pour toutes les vulnérabilités
def scan_page(page) :

    print(f"\nAnalyse de la page : {page}")
    sqli = test_sql_injection(page)
    xss = test_xss(page)
    headers = check_security_headers(page)
    files = check_exposed_files(page)
    dirs = check_directory_listing(page)
    csrf_forms = check_csrf_forms(page)

    return {
        "url": page,
        "sqli": [p for _, p in sqli],
        "xss": xss,
        "headers": list(headers.keys()),
        "exposed_files": files,
        "directory_listing": dirs,
        "csrf": csrf_forms
    }


def main() :
    logger.info("=== FlowScanner — Scanner de vulnérabilités Web ===\n")
    raw_url = input("Entrez l'URL cible à analyser : ")
    target_url = format_url(raw_url)

    if not is_valid_url(target_url):
        logger.error("URL invalide")
        print("URL invalide. Exemple attendu : https://example.com")
        return
    

    logger.info(f"Crawling de : {target_url}")

    pages = crawl(target_url, max_pages=30, delay=0.7, verbose=True)
    logger.info(f"{len(pages)} pages trouvées")

    scan_results = []
    for page in pages:
        logger.info(f"Analyse de : {page}")
        result = scan_page(page)
        scan_results.append(result)

    logger.info("Analyse terminé. Génération du rapport HTML...")
    generate_html_report(scan_results)
    logger.info("Rapport généré")




if __name__ == "__main__":
    main()
