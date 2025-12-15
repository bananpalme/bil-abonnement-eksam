# 💸 Damage Service (Digital Skadesvurdering & Prisestimater)

Denne Microservice er ansvarlig for at håndtere registrering, klassificering og prissætning af nye skader konstateret på udlejningsbilerne. Servicen sikrer, at skadesprocessen er standardiseret og giver et datagrundlag for kommunikation med kunder og forsikringsselskaber.

## 🌟 Formål

Hovedformålet med Damage Service er at:
1.  **Standardisere Prissætning:** Opretholde en central liste over skadetyper og deres basisomkostninger.
2.  **Digital Skadesregistrering:** Modtage og gemme oplysninger om nye skader, herunder hvilken bil de vedrører, og hvad den estimerede pris er.
3.  **Rapportering:** Levere aggregeret data om totale skadesomkostninger pr. bil til brug i dashboards og kundekommunikation.
4.  **Integration:** Give Inspection Service mulighed for at registrere skader og UI Service mulighed for at præsentere dem.

## 🏗️ Arkitektur og Persistens

| Parameter | Værdi | Bemærkning |
| :--- | :--- | :--- |
| **Teknologi** | Python, Flask | Letvægts API. |
| **Database** | **SQLite** | Anvendes til udvikling og test. Gemmer tabellerne `damage_types` og `car_damages`. |
| **Persistens** | Docker Volume | Sikrer, at data (f.eks. basisomkostninger og registrerede skader) bevares. |
| **Port** | 5004 | Standard intern port i Docker Compose. |
| **Afhængigheder** | Kræver et **JWT-token** (fra Account Service) for at tilgå beskyttede endpoints. |

## 🛠️ Nøgle API Endpoints

Disse endpoints tilgås via **API Gateway** på port **5000**.

| Route | Metode | Beskrivelse | Nøglefunktion & Payload |
| :--- | :--- | :--- | :--- |
| `/api/damage-types` | `GET` | Henter den komplette liste over standardiserede skadetyper og deres basisomkostninger. | **Prisliste** (Basis for skadesvurdering) |
| `/api/car-damages` | `POST` | Registrerer én eller flere nye skader på en bil. Bruges typisk efter inspektion. | **Skadesregistrering** Payload: `[ { "car_id": 1, "damage_type_id": 5, "cost_at_time": 650 }, ... ]` |
| `/api/car-damages` | `GET` | Henter en aggregeret rapport, der viser de totale skadesomkostninger, fordelt pr. bil (ID). | **Rapportering** |

## 🗃️ Datastruktur

Servicen vedligeholder to centrale datatabeller:

1.  **`damage_types`**: Indeholder basisinformation om skader (f.eks. "Scratch", "Dent") og den standardiserede `base_cost`.
2.  **`car_damages`**: Logger hvilke skadetyper der er registreret på specifikke biler (`car_id`) og den præcise `cost_at_time` (da prisen kan ændre sig over tid).

### Kørsel (via Docker Compose)

Damage Service køres automatisk som en del af den overordnede Docker Compose-opsætning og lytter internt på port **5004**.

```bash
# Fra roden af dit projekt (hvor docker-compose.yaml ligger):
docker-compose up -d --build
```

Alternativt hvis det skal køres lokalt
```bash
# fra DamageService folderen ./DamageService/
python app.py
```
