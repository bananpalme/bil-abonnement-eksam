# 🔑 Return Service (Digital Afleveringslog & Bekræftelse)

Denne microservice er kernen i den kontaktløse afleveringsproces. Dens primære ansvar er at digitalisere og automatisere de første trin i bilafleveringen, fra kunden slipper nøglen i boksen, til medarbejderen henter den.

## 🌟 Formål

Hovedformålet med Return Service er at sikre:
1.  **Registrering af Afleveringstidspunkt:** Systemet logger automatisk det præcise tidspunkt for kundens aflevering via appen.
2.  **Datapersistens:** Sikker lagring af nøgleinformation (Nummerplade, Kontrakt-ID).
3.  **Transparens:** Afsendelse af bekræftelse til kunden, når nøglen officielt er modtaget af en medarbejder.

## 🏗️ Arkitektur og Persistens

| Parameter | Værdi | Bemærkning |
| :--- | :--- | :--- |
| **Teknologi** | Python, Flask | Letvægts API. |
| **Database** | **SQLite** | Valgt til udvikling og test for nem opsætning. |
| **Port** | 5002 | Standard intern port i Docker Compose. |

## 🛠️ Nøgle API Endpoints

Disse endpoints tilgås via **API Gateway** på port **5000**.

| Route | Metode | Beskrivelse | Nøglefunktion & Payload |
| :--- | :--- | :--- | :--- |
| `/api/return/log` | `POST` | Kundens registrering af nøgleaflevering via appen. Opretter en ny log i databasen med status: *"Key dropped in box"*. | **Kundelogning** Payload: `{ "license_plate": "...", "contract_id": "..." }` |
| `/api/return/key_pickup` | `POST` | Bruges af medarbejderen (via internt system) til at bekræfte, at nøglen fysisk er afhentet. Opdaterer loggen til *"Key picked up by employee"* og sender besked til kunden. | **Medarbejderbekræftelse** Payload: `{ "log_id": 123, "employee_id": 456 }` |
| `/api/returns` | `GET` | Henter en historisk liste over alle bilafleveringer i systemet. | **Historisk Data** (Kræver JWT) |

## 🚀 Kom godt i gang

### Kørsel (via Docker Compose)

Return Service køres automatisk som en del af den overordnede Docker Compose-opsætning.

```bash
# Fra roden af dit projekt (hvor docker-compose.yaml ligger):
docker-compose up -d --build
```

Ellers kør det manuelt på port 5002

```bash
# Kør det i ReturnService folderen
python app.py
```
