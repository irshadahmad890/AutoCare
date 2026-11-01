# AutoCare – Garage Management System

AutoCare is a garage management system designed to help independent vehicle service centers manage their daily operations, including customers, vehicles, repair jobs, mechanics, spare parts, and payments.

The project aims to replace manual garage records with a centralized digital system where garage staff can manage repair workflows and customers can track their vehicle service progress.

**Project Status:** Early Development – Django project structure and initial database models are being implemented.

---

## Current Implementation

The following components are currently present in the project:

| Module          | Implementation                                       |
| --------------- | ---------------------------------------------------- |
| Custom User     | Custom Django user model with email, phone, and role |
| Customers       | Customer information and contact details             |
| Vehicles        | Vehicle information linked to customers              |
| Repair Jobs     | Job number, vehicle, description, and status         |
| Mechanics       | Mechanic profiles and hourly rates                   |
| Job Assignments | Multiple mechanics assigned to one job               |
| Parts           | Spare parts catalogue and stock quantity             |
| Job Parts       | Parts and quantities associated with repair jobs     |
| Payments        | App structure created; implementation pending        |

**Note:** These are initial database models. REST APIs, business logic, frontend functionality, and complete workflows are still under development.

---

## Repair Workflow

The intended repair workflow:

1. Register a customer.
2. Register the customer's vehicle.
3. Create a repair job for the vehicle.
4. Inspect the vehicle and identify required repairs.
5. Prepare an itemized repair estimate.
6. Send the estimate to the customer for approval.
7. Assign one or more mechanics to the repair job.
8. Record mechanic working hours.
9. Record spare parts used during repairs.
10. Update repair progress and upload photos.
11. Complete the repair job.
12. Generate the final invoice.
13. Record customer payment.
14. Maintain the vehicle's service history.

---

## Database Relationships

The current database design includes the following relationships:

| Relationship       | Description                                                         |
| ------------------ | ------------------------------------------------------------------- |
| Customer → Vehicle | One customer can have multiple vehicles.                            |
| Vehicle → Job      | One vehicle can have multiple repair jobs.                          |
| Job ↔ Mechanic     | Multiple mechanics can work on multiple jobs through `JobMechanic`. |
| Job ↔ Part         | Multiple parts can be used in multiple jobs through `JobPart`.      |
| User → Mechanic    | A user can have one mechanic profile.                               |

### Important Database Design Decisions

**JobMechanic**

This intermediate model stores:

- Job
- Mechanic
- Working hours
- Assignment date

It allows multiple mechanics to work on the same repair job.

**JobPart**

This intermediate model stores:

- Job
- Part
- Quantity
- Unit price

It records which parts are used for each repair job and preserves the unit price recorded at the time of use.

---

## Technology Stack

### Backend

- Python
- Django
- Django REST Framework
- Django REST Framework Simple JWT
- MySQL
- mysqlclient
- python-decouple

### Development Tools

- Visual Studio Code
- Git and GitHub
- MySQL Workbench
- Postman

The frontend will be developed after the backend APIs and core business logic are ready.

---

## Project Structure

```text
AutoCare/
│
├── client/
│   └── # Frontend application (planned)
│
├── server/
│   │
│   ├── apps/
│   │   ├── user/
│   │   ├── customers/
│   │   ├── vehicle/
│   │   ├── job/
│   │   ├── mechanics/
│   │   ├── parts/
│   │   └── payments/
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   └── manage.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Local Development Setup

### Prerequisites

Before running the project, install:

- Python
- MySQL Server
- Git
- Visual Studio Code

---

## Development Roadmap

### Phase 1 – Project Setup and Database Design

- [✅] Create Django project structure.
- [✅] Established Project applications.
- [✅] Define the Database Schema 
- [✅] Create the models for applications
- [✅] Build the relationship between models
- [✅] Review and finalize database relationships.
- [✅] Complete database migrations.


---

## Repository

**GitHub:** [https://github.com/irshadahmad890/AutoCare](https://github.com/irshadahmad890/AutoCare)

**Developer:** Irshad Ahmad

**Project:** AutoCare – Garage Management System

**Status:** Under Development
