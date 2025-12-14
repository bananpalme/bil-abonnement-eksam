# Brug et officielt Python runtime som base image
FROM python:3.11-slim

# Sæt arbejdsmappe i containeren
WORKDIR /app

# Kopier filen med afhængigheder
# Antager, at du har lavet en samlet requirements.txt i roden af projektet
# Hvis requirements.txt er i denne mappe, skal du kun skrive 'COPY requirements.txt .'
COPY requirements.txt .

# Installer Python-afhængigheder (Flask, Streamlit, requests mv.)
RUN pip install --no-cache-dir -r requirements.txt

# Kopier hele app-mappen ind i containeren (inkl. pages/)
COPY . .

# Streamlit kører som standard på port 8501
EXPOSE 8501

# Definer kommandoen, der skal køre Streamlit-appen med pages
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]