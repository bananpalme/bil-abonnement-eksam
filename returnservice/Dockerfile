# Dockerfile i returnservice mappen
FROM python:3.9

WORKDIR /app

# VIGTIGT: Antager, at requirements.txt kopieres ind i konteksten af byggeprocessen
# Ellers skal du bruge COPY ../requirements.txt .
COPY requirements.txt . 
RUN pip install -r requirements.txt

# Kopierer koden (app.py og database.py) ind
COPY . .

# Korrekt eksponering for Flask standardport
EXPOSE 5000 

CMD ["python", "app.py"]
