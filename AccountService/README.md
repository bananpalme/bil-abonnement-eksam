# 🔑 Account Service (Authentication & JWT Management)

Denne microservice er ansvarlig for al brugerautentifikation og udstedelse af JSON Web Tokens (JWT) i Bilabonnement-systemet. Servicen fungerer som den centrale adgangskontrolport for alle andre Microservices.

## 🌟 Formål

Hovedformålet med Account Service er at:
1. **Autentificere** brugere (medarbejdere og kunder) baseret på legitimationsoplysninger.
2. **Udstede JWT-tokens** ved vellykket login for at give adgang til systemet.
3. Fungerer som den centrale kilde for **adgangskontrol (Auth)**, som API Gateway kan validere tokens imod.

## 🏗️ Arkitektur og Persistens

| Parameter | Værdi | Bemærkning |
| :--- | :--- | :--- |
| **Teknologi** | Python, Flask | Letvægts API til hurtig autentifikation. |
| **Sikkerhed** | JWT | Håndtering af sikre, signerede JSON Web Tokens. |
| **Database** | **SQLite** | **Valgt til udvikling og test** for at sikre en filbaseret, nem opsætning i Docker Compose. |
| **Port** | 5002 | Standard intern port i Docker Compose. |


## 🛠️ Nøgle Endpoints

Disse endpoints tilgås via **API Gateway** på port **5000**.

| Route | Metode | Beskrivelse | Payload |
| :--- | :--- | :--- | :--- |
| `/api/login` | `POST` | Autentificerer en bruger og returnerer et signeret JWT. | Login & JWT Udstedelse Payload: { "username": "...", "password": "..." }|
| `/api/profile ` | `POST` | Registrerer en ny brugerkonto (username, password, role) i databasen. (Bruges typisk til systemopsætning). | `{ Brugerregistrering Payload: { "username": "...", "password": "...", "role": "..." }` |
| `/api/profile ` | `GET ` | Kræver et gyldigt JWT-token. Henter den aktuelle brugers profilinformation (username, id, role).. | Beskyttet Ressource (Kræver JWT i headeren)|


### Kørsel (via Docker Compose)

Account Service køres automatisk som en del af den overordnede Docker Compose-opsætning og lytter internt på port **5002**.

```bash
# Fra roden af dit projekt (hvor docker-compose.yaml ligger):
docker-compose up -d --build
```

Alternativt hvis det skal køres lokalt
```bash
# fra AccountService folderen ./AccountService/
python app.py
```
