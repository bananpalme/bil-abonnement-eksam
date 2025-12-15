# 🌐 API Gateway (Trafikstyring & Single Entry Point)

API Gateway er det eneste adgangspunkt for eksterne klienter (som UI Service og Mobile App) til Microservice-arkitekturen. Den varetager trafikdirigering, samler endpoints fra de forskellige services og sikrer, at forespørgsler kan krydse serviceniveauet gnidningsfrit. 

[Image of Microservice API Gateway Architecture]


## 🌟 Formål

Hovedformålet med API Gateway er at:
1.  **Trafikdirigering (Routing):** Videresende indgående requests til den korrekte Microservice baseret på URL-stien.
2.  **Aggregation:** Samle logik og data fra flere Microservices, så klienten kun behøver at kende ét endpoint.
3.  **Sikkerhedsbekymringer:** Håndtere JWT-validering og videresende Authorization-headers til de beskyttede Microservices.
4.  **Miljøkonfiguration:** Læse de interne service-URL'er fra miljøvariabler (Docker Compose) for at sikre fleksibilitet.

## 🏗️ Arkitektur og Konfiguration

| Parameter | Værdi | Bemærkning |
| :--- | :--- | :--- |
| **Teknologi** | Python, Flask | Simpel og letvægts routing-implementering. |
| **Port** | 5000 | Ekstern port for alle klienter. |
| **Service URLs** | Miljøvariabler | Læser interne URLs (f.eks. `RENTAL_SERVICE_URL`) fra Docker Compose for at finde Microservices. |
| **Sikkerhed** | Authorization Header | Videresender `Authorization: Bearer <token>` til Microservices, der kræver det. |

## 🛠️ Nøgle Endpoints (Routing Oversigt)

API Gateway samler og dirigerer requests til 5 forskellige Microservices.

### A. Rental Service (Stamdata & Kontrakter)

| Klient Endpoint | Metode | Dirigeres til | Formål |
| :--- | :--- | :--- | :--- |
| `/api/client` | `GET` | `RENTAL_SERVICE_URL/client` | Henter alle kunder. |
| `/api/client/<id>` | `GET` | `RENTAL_SERVICE_URL/client/<id>` | Henter specifik kunde. |
| `/api/cars` | `GET` | `RENTAL_SERVICE_URL/cars` | Henter bilflåden. |
| `/api/contract` | `POST`/`GET` | `RENTAL_SERVICE_URL/contract` | Opretter / Henter kontrakter. |

### B. Account Service (Autentifikation)

| Klient Endpoint | Metode | Dirigeres til | Formål |
| :--- | :--- | :--- | :--- |
| `/api/login` | `POST` | `ACCOUNT_SERVICE_URL/login` | Udsteder JWT-token ved login. |
| `/api/profile` | `POST` | `ACCOUNT_SERVICE_URL/profile` | Registrerer ny bruger. |
| `/api/profile` | `GET` | `ACCOUNT_SERVICE_URL/profile` | Henter brugerprofil (beskyttet). |

### C. Return Service (Afleveringslogik)

| Klient Endpoint | Metode | Dirigeres til | Formål |
| :--- | :--- | :--- | :--- |
| `/api/return/log` | `POST` | `RETURN_SERVICE_URL/return/log` | Logger kundens nøgleaflevering. |
| `/api/return/key_pickup` | `POST` | `RETURN_SERVICE_URL/return/key_pickup` | Medarbejder bekræfter afhentning. |

### D. Inspection Service (Inspektionsdata)

| Klient Endpoint | Metode | Dirigeres til | Formål |
| :--- | :--- | :--- | :--- |
| `/api/inspection` | `POST` | `INSPECTION_SERVICE_URL/inspection` | Starter/registrerer ny inspektion. |
| `/api/inspection/<id>` | `GET` | `INSPECTION_SERVICE_URL/inspection/<id>` | Henter specifik inspektionsrapport. |

### E. Damage Service (Skadesregistrering)

| Klient Endpoint | Metode | Dirigeres til | Formål |
| :--- | :--- | :--- | :--- |
| `/api/damage-types` | `GET` | `DAMAGE_SERVICE_URL/damage-types` | Henter skadeprislisten. |
| `/api/car-damages` | `GET` | `DAMAGE_SERVICE_URL/car-damages` | Henter samlede skader pr. bil. |
| `/api/car-damages` | `POST` | `DAMAGE_SERVICE_URL/car-damages` | Registrerer ny skade. |

## 🚀 Kom godt i gang

API Gateway startes automatisk via Docker Compose og lytter på `http://localhost:5000`.

```bash
# Fra roden af dit projekt (hvor docker-compose.yaml ligger):
docker-compose up -d --build
```

Ellers kør det lokalt på port localhost:5000
```bash
# Kør det i ApiGateway folderen
python app.py
```
