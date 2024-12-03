FROM python:3.8-slim

WORKDIR /usr/share/flask-app

# Copier les fichiers nécessaires dans l'image
COPY general/app.py /usr/share/flask-app/
COPY general/templates /usr/share/flask-app/templates/

# Installer Flask
RUN pip install --no-cache-dir Flask

# Exposer le port 5000
EXPOSE 5000

# Lancer l'application Flask
CMD ["python", "app.py"]
