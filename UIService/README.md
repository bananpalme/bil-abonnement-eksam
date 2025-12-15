# 🖥️ UI Service (Streamlit Dashboard)

Denne Microservice fungerer som systemets frontend og dashboard. Den er bygget med Streamlit og giver et brugervenligt interface for medarbejdere og administratorer til at interagere med de underliggende Microservices (Rental, Inspection, Damage, Return) via **API Gateway**.

## 🌟 Formål

Hovedformålet med UI Service er at:
1.  **Brugergrænseflade:** Fungerer som den visuelle grænseflade, der samler funktionalitet fra hele systemet.
2.  **Autentifikation:** Håndtere login, sessionsstyring og tokenlagring via Streamlit Session State.
3.  **Rollebaseret Adgang:** Styre, hvilke funktioner og sider brugeren kan se, baseret på den tildelte rolle (`dataregistry`, `damages`, `admin`).
4.  **Integration:** Kommunikere udelukkende med API Gateway for at undgå direkte afhængighed af individuelle Microservices.

## 🏗️ Arkitektur og Konfiguration

| Parameter | Værdi | Bemærkning |
| :--- | :--- | :--- |
| **Teknologi** | Python, Streamlit | Bruges for hurtig udvikling af datadrevne dashboards. |
| **Kommunikation** | Requests | Bruger `requests` til at sende alle API-kald via Gatewayen. |
| **Port** | 8501 | Standard ekstern port for Streamlit. |
| **Miljøvariabel** | `API_GATEWAY_URL` | Læses fra Docker Compose for at finde Gatewayens adresse. |

## 🛠️ Nøglefunktionalitet

Applikationen er bygget op omkring en central autentifikationsmekanisme:

### 1. Login og Registrering

* **Login:** Sender brugernavn og password til `/api/login` (via Gateway). Gemmer det modtagne `access_token` og `role` i Streamlit Session State.
* **Registrering:** Tillader oprettelse af nye brugere (medarbejdere) med tildelt rolle via `/api/profile` POST-endpointet.

### 2. Sessionsstyring

* Bruger **Streamlit Session State** til at holde styr på brugerens login-status (`logged_in`), `token`, `username` og `role`.
* Viser kun navigation og funktionalitet, hvis `logged_in` er sand.
* Giver mulighed for **Logout** i sidebar.

### 3. Rollebaseret Adgang

* Når en bruger er logget ind, præsenteres de for dashboards og funktioner, der passer til deres rolle:
    * **`dataregistry`**: Adgang til Rental Service (Kontraktregistrering).
    * **`damages`**: Adgang til Damage Service (Skadesregistrering).
    * **`admin`**: Fuld adgang til alle systemfunktioner.

## 🚀 Kom godt i gang

### Kørsel (via Docker Compose)

UI Service startes automatisk via Docker Compose og er tilgængelig i browseren.

```bash
# Fra roden af dit projekt:
docker-compose up -d --build

# Åbn i browseren:
http://localhost:8501
