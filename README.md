# ⚙️ Inspection Service (Standardiseret Bilinspektion)

Denne Microservice er designet til at understøtte medarbejdernes inspektionsproces efter, at bilen er blevet afleveret via Return Service. Servicen leverer et standardiseret format for dataregistrering, hvilket sikrer ensartethed og fuld dokumentation af bilens stand.

## 🌟 Formål

Hovedformålet med Inspection Service er at:
1.  **Standardisere Tjeklisten:** Sikre, at alle medarbejdere følger den samme faste procedure for inspektion af bilens interiør og eksteriør.
2.  **Dokumentere Stand:** Registrere kilometerstand, stand på sæder, rat, mv., og fungere som lagringspunkt for fotodokumentation.
3.  **Forberede Skadesvurdering:** Sammenligne den aktuelle stand med data om tidligere registrerede skader.
4.  **Data til Næste Trin:** Levere strukturerede data direkte til Damage Service, hvis der konstateres nye skader.

## 🏗️ Arkitektur og Persistens

| Parameter | Værdi | Bemærkning |
| :--- | :--- | :--- |
| **Teknologi** | Python, Flask | Letvægts API. |
| **Database** | **SQLite** | Valgt til udvikling og test for nem opsætning. |
| **Persistens** | Docker Volume | Sikrer, at de registrerede inspektionslogninger bevares. |
| **Port** | 5003 | Standard intern port i Docker Compose. |

## 🛠️ Nøgle API Endpoints

Disse endpoints tilgås via **API Gateway** på port **5000**.

| Route | Metode | Beskrivelse | Nøglefunktion & Payload |
| :--- | :--- | :--- | :--- |
| `/api/inspection/` | `POST` | Medarbejderen starter en ny, standardiseret inspektionsrunde og registrerer alle tjeklistepunkter (interiør, kilometerstand). | **Opret Inspektion** Payload: Inkluderer alle tjeklistepunkter (f.eks. `km_after`, `seats_ok`, `warning_lights_ok`). |
| `/api/inspection/<id>` | `GET` | Henter en specifik inspektionsrapport ved ID. Bruges til at se historik og sammenligne stand. | **Hent Rapport** Kræver gyldigt JWT i header. |

## 🗃️ Datastruktur

Servicen gemmer data i tabellen `inspections`, som indeholder felter for bilinformation (`car_number`, `km_before`, `km_after`) og en række boolske felter (`seats_ok`, `steering_ok`, etc.), der sikrer den standardiserede tjekliste.
