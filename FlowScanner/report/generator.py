# report/generator.py

import webbrowser
from pathlib import Path
from datetime import datetime

def generate_html_report(results, filename="rapport.html"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Rapport de vulnérabilités</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        .vuln {{ background: #ffe6e6; border-left: 5px solid red; padding: 10px; margin-bottom: 20px; }}
        .ok {{ background: #e6ffe6; border-left: 5px solid green; padding: 10px; margin-bottom: 20px; }}
        code {{ background: #eee; padding: 2px 4px; border-radius: 4px; }}
    </style>
</head>
<body>
    <h1>🔎 Rapport de scan - {now}</h1>
"""

    for page in results:
        html += f"<h2>Page : <a href='{page['url']}'>{page['url']}</a></h2>"

        if page['sqli']:
            html += "<div class='vuln'><strong>Injection SQL détectée :</strong><ul>"
            for payload in page['sqli']:
                html += f"<li><code>{payload}</code></li>"
            html += "</ul></div>"
        else:
            html += "<div class='ok'>✅ Aucune injection SQL détectée</div>"

        if page['xss']:
            html += "<div class='vuln'><strong>XSS détectée :</strong><ul>"
            for payload in page['xss']:
                html += f"<li><code>{payload}</code></li>"
            html += "</ul></div>"
        else:
            html += "<div class='ok'>✅ Aucune XSS détectée</div>"
        #
        if page['headers']:
            html += "<div class='vuln'><strong>Headers manquants :</strong><ul>"
            for h in page['headers']:
                html += f"<li>{h}</li>"
            html += "</ul></div>"
        else:
            html += "<div class='ok'>✅ Tous les headers importants sont présents</div>"
        # Fichiers exposés
        if page.get('exposed_files'):
            html += "<div class='vuln'><strong>Fichiers sensibles accessibles :</strong><ul>"
            for f in page['exposed_files']:
                html += f"<li><a href='{f}' target='_blank'>{f}</a></li>"
            html += "</ul></div>"
        else:
            html += "<div class='ok'>✅ Aucun fichier sensible détecté</div>"

        html += "<hr>"
        # Directory listing
        if page.get('directory_listing'):
            html += "<div class='vuln'><strong>Directory listing activé :</strong><ul>"
            for d in page['directory_listing']:
                html += f"<li><a href='{d}' target='_blank'>{d}</a></li>"
            html += "</ul></div>"
        else:
            html += "<div class='ok'>✅ Aucun répertoire listé trouvé</div>"
        # CSRF
        if page.get("csrf"):
            html += "<div class='vuln'><strong>Formulaires POST sans token CSRF :</strong><ul>"
            for form_snippet in page["csrf"]:
                html += f"<li><code>{form_snippet}</code></li>"
            html += "</ul></div>"
        else:
            html += "<div class='ok'>✅ Tous les formulaires POST contiennent un token CSRF</div>"


    html += "</body></html>"

    # Écriture du fichier HTML
    path = Path(filename)
    path.write_text(html, encoding="utf-8")

    # Ouverture dans le navigateur
    webbrowser.open(str(path.resolve()))
