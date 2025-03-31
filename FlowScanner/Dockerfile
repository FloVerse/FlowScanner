# Dockerfile

# 1. Utilisation d'une image Python légère
FROM python:3.11-slim

# 2. Dossier de travail
WORKDIR /app

# 3. Copier les fichiers du projet
COPY . /app

# 4. Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# 5. Définir la commande par défaut
CMD ["python", "main.py"]
