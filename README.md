# FlowScanner – Scanner de vulnérabilités Web

FlowScanner est un outil d’analyse de sécurité web développé en **Python** qui permet de détecter automatiquement les vulnérabilités les plus courantes listées dans l’**OWASP Top 10**.

---

## Fonctionnalités

- Crawling automatique des pages d'un site web  -
- Détection d'**injection SQL**  
- Détection de vulnérabilités **XSS (Cross-Site Scripting)**  
- Vérification des **headers de sécurité HTTP**  
- Recherche de **fichiers sensibles exposés**  
- Détection de **directory listing**  
- Analyse des **formulaires POST sans protection CSRF**  
- **Génération automatique d’un rapport HTML interactif**  
- **Logs complets** de l’analyse  
- **Dockerisation** pour une utilisation facile et portable

---

## 📂 Structure du projet

vulnscanner/

main.py                  # Lancement du scanner

├── logger.py                # Système de logs

├── scanner/ # Modules de scan

│   ├── crawler.py

│   ├── sql_injection.py

│   ├── xss_checker.py

│   ├── headers_checker.py

│   ├── exposed_files.py

│   ├── directory_listing.py

│   └── csrf_checker.py

├── report/                  # Génération du rapport

│   └── generator.py

├── requirements.txt         # Dépendances Python

├── Dockerfile               # Dockerisation

└── README.md                # Documentation

---

## Installation

### Prérequis
- Python ≥ 3.9 **ou**
- Docker Desktop

---

### Utilisation sans Docker

1. Clonez le projet :

```bash
git clone https://github.com/ton_pseudo/vulnscanner.git
cd vulnscanner
```
2. Création d'un environnement virtuel et installation des dépendances :

```bash
python -m venv .venv
source .venv/bin/activate   # Sur Windows : .venv\Scripts\activate
pip install -r requirements.txt
```
3. Lancement du scanner
```bash
python main.py
```
### Utilisation avec Docker

1. Construisez l'image Docker :

```bash
docker build -t vulnscanner .
```

2. Lancez le scanner :

```bash
docker run -it vulnscanner
```

## Exemple de rapport
À la fin de l’analyse, un fichier rapport.html sera généré automatiquement et ouvert dans votre navigateur.

###Le rapport contient :

- Toutes les pages explorées
- Vulnérabilités détectées (SQL Injection, XSS, Headers manquants, CSRF, fichiers exposés, directory listing)
- Résumé clair et structuré des risques identifiés

## Évolutions à venir...

- Ajout d’un système de scoring
- Export du rapport en PDF
- Interface CLI avancée
- Dashboard web (Flask)
