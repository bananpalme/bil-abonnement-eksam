# Brug et officielt Python runtime som base image
FROM python:3.11-slim

# Sæt arbejdsmappe i containeren
WORKDIR /app

# Kopier filen med afhængigheder. Antager, at requirements.txt findes i denne mappe
# Hvis du har en samlet requirements.txt i roden, skal du justere stien.
COPY requirements.txt .

# Installer Python-afhængigheder (Flask, sqlite3 mv.)
RUN pip install --no-cache-dir -r requirements.txt

# Kopier alle de nødvendige filer ind i containeren
# Inkluderer app.py og database.py
COPY . .

# Kør database-setup ved at kalde database.py direkte
# Dette sikrer, at databasen og tabellen 'inspections' oprettes før appen starter.
RUN python database.py

# INSPECTION SERVICE kører på port 5003 (som defineret i app.py)
EXPOSE 5003

# Definer kommandoen, der skal køre Flask-applikationen
# Vi bruger 'python app.py' som startkommando
CMD ["python", "app.py"]