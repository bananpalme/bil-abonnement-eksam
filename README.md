# Bilabonnement - Digitaliseret Retursystem (Microservice Projekt)

Dette projekt implementerer en Microservice-baseret løsning, der digitaliserer og automatiserer den komplette proces for bilaflevering, inspektion og skadehåndtering. Målet er at transformere manuelle arbejdsgange til et effektivt, datadrevet flow, som opfylder kravene til **Dataregistrering** og gennemsigtighed i hele lejeaftalens afslutning.

## 🌟 Formål

Systemet adresserer de nuværende udfordringer ved at aflever og skaber:
1.  **Kontaktløs Aflevering:** Giver kunden fleksibilitet 24/7 og registrerer automatisk det præcise afleveringstidspunkt.
2.  **Standardiseret Inspektion:** Garanterer ensartethed i medarbejderens kontrol og dokumentation for at reducere fejl og uenigheder.
3.  **Digital Skadehåndtering:** Etablerer et transparent datagrundlag med billeder og prisestimater pr. fejl, der er tilgængeligt for både internt personale og eksterne partnere.

## 🏗️ Arkitektur Oversigt

Systemet består af seks specialiserede Microservices, som orkestreres via en API Gateway. Hver service har et unikt, afgrænset ansvarsområde (Single Responsibility Principle). 

| Service | Teknologi | Hovedansvar |
| :--- | :--- | :--- |
| **UI Service** | Streamlit | Frontend til test og demonstration af brugerflow (Kunde/Medarbejder). |
| **API Gateway** | Flask/Python | Router trafikken, centraliserer adgangskontrol og fungerer som single entry point. |
| **Account Service** | Flask/JWT | Håndterer **Login**, **Account Database** og udstedelse/validering af **JWT Tokens**. |
| **Rental Service** | Flask/SQLAlchemy | Håndterer oprettelse af **nye lejeaftaler** og stamdata. |
| **Return Service** | Flask/SQLAlchemy | Håndterer afleveringsprocessen: Logger tidspunkt, modtager oplysninger og bekræfter nøgleafhentning til kunden. |
| **Inspection Service** | Flask/Python | Leverer den **standardiserede tjekliste** til medarbejderen (eksteriør, interiør, kilometerstand) og sammenligner med tidligere registrerede skader. |
| **Damage Service** | Flask/SQLAlchemy | Håndterer oprettelse af **digitale skadesrapporter**. Vurderer udgifter (pris pr. fejl) og lagrer dokumentation. |

## 🚀 Kom godt i gang

Disse instruktioner antager, at du har **Docker** og **Docker Compose** installeret.

### 1. Byg og Kør Systemet

Naviger til roden af projektet (hvor `docker-compose.yaml` ligger) og kør:

```bash
docker-compose up -d --build
