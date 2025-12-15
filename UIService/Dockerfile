# Brug et officielt Python runtime som base image
FROM python:3.11-slim

# Sæt arbejdsmappe i containeren
WORKDIR /app

# Kopier filen med afhængigheder. 
# Antager, at requirements.txt findes i denne mappe og indeholder Streamlit og requests.
COPY requirements.txt .

# Installer Python-afhængigheder
RUN pip install --no-cache-dir -r requirements.txt

# Kopier alle kildekoder (f.eks. ui.py) ind i containeren
COPY . .

# Streamlit kører som standard på port 8501
EXPOSE 8501

# Definer kommandoen, der skal køre Streamlit-appen
# Vi sikrer, at den lytter på 0.0.0.0, så den er tilgængelig via Docker-netværket
# CMD ["streamlit", "run", "din_streamlit_fil.py", "--server.port=8501", "--server.address=0.0.0.0"]
# OBS: Hvis din hovedfil hedder 'ui.py', skal du rette kommandoen:
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]