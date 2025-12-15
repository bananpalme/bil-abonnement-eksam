# ✍️ Rental Service (Kontrakt- og Stamdatahåndtering)

Denne Microservice er ansvarlig for at styre kernedataene i Bilabonnements forretning: Klientinformation, bilflåden og oprettelsen af nye lejeaftaler. Servicen fungerer som den primære datakilde for stamdata i systemet.

## 🌟 Formål

Hovedformålet med Rental Service er at:
1.  **Stamdatahåndtering:** Levere opdaterede lister over kunder og bilflåde til andre services.
2.  **Kontraktregistrering:** Oprette nye lejeaftaler, herunder beregning af samlede omkostninger baseret på månedlig rate og varighed.
3.  **Dataudstilling:** Udstille klient- og bilinformation til UI'et for medarbejdere, der skal oprette kontrakter.

## 🏗️ Arkitektur og Persistens

| Parameter | Værdi | Bemærkning |
| :--- | :--- | :--- |
| **Teknologi** | Python, Flask | Letvægts API. |
| **Database** | **SQLite** | Anvendes til udvikling og test. Gemmer tabellerne `clients`, `cars`, og `rentals`. |
| **Port** | 5001 | Standard intern port i Docker Compose. |
| **Sikkerhed** | Kræver **JWT-token** for alle endpoints. |

## 🛠️ Nøgle API Endpoints

Disse endpoints tilgås via **API Gateway** på port **5000**.

| Route | Metode | Beskrivelse | Nøglefunktion & Payload |
| :--- | :--- | :--- | :--- |
| `/api/client` | `GET` | Henter en liste over alle registrerede kunder. | **Stamdata** |
| `/api/client/<id>` | `GET` | Henter detaljeret information om en specifik kunde. | **Stamdata** |
| `/api/cars` | `GET` | Henter en liste over alle biler i flåden, inkl. status (f.eks. 'available', 'rented'). | **Stamdata** |
| `/api/contract` | `POST` | **Opretter en ny lejeaftale.** Beregner `total_cost` automatisk. | **Kontraktregistrering** Payload: `{ "client_id": 1, "car_id": 10, "months": 12, "monthly_rate": 2500.00 }` |
| `/api/contract` | `GET` | Henter en liste over alle eksisterende lejeaftaler. | **Rapportering** |

## 🗃️ Datastruktur

Servicen vedligeholder tre centrale tabeller i sin SQLite-database:

1.  **`clients`**: Basisinformation om kunder.
2.  **`cars`**: Information om bilflåden.
3.  **`rentals`**: Relationel data, der forbinder `client_id` og `car_id` med aftalevilkår (`months`, `monthly_rate`).
