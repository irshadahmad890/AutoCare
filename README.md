
# 🚗 AutoCare – Garage Management SaaS

**AutoCare** is a full-stack garage management application designed to digitize and simplify daily operations for independent automobile workshops and service centers.

It replaces manual registers, notebooks, and disconnected spreadsheets with a centralized platform where garage administrators can manage customers, vehicles, mechanics, repair jobs, spare parts, invoices, and payments.

Customers can access their vehicles, monitor repair progress, view service information, and manage their interactions with the garage.

## 🌐 Live Application

- **Frontend:** https://autocare-murex.vercel.app/
- **Backend:** Django REST Framework API (Need Paid Server for Storage Media and Database Space)
- **Repository:** https://github.com/irshadahmad890/AutoCare

## 🎯 Problem & Solution

Many independent garages still depend on manual records to manage their daily operations.

This creates problems such as:

- Difficulty tracking vehicle repair progress.
- Disorganized customer and vehicle records.
- Poor communication between mechanics and customers.
- Errors in repair estimates, invoices, and payments.
- Difficulty maintaining vehicle service history.

AutoCare provides a centralized digital solution to manage these operations efficiently.

## ✨ Core Features

### 1. Authentication & User Management
- Customer registration and login.
- JWT-based authentication.
- Role-based access control.
- Separate access for administrators, mechanics, and customers.
- Secure account management.

### 2. Customer Management
- Create, view, update, and manage customer records.
- Store customer contact information.
- Manage customer-specific vehicle records.
- Restrict customer access to their own information.

### 3. Vehicle Management
- Register and manage customer vehicles.
- Maintain vehicle information.
- Associate vehicles with their respective customers.
- Access vehicle service history.

### 4. Repair & Job Management
- Manage vehicle repair jobs.
- Track repair status.
- Assign mechanics to repair jobs.
- Manage repair information and job progress.

### 5. Mechanic Management
- Create and manage mechanic profiles.
- Manage mechanic specializations.
- Assign multiple mechanics to repair jobs.
- Track mechanic assignments.

### 6. Spare Parts & Inventory
- Manage spare parts records.
- Maintain part quantities and prices.
- Associate parts with repair jobs.
- Track parts used during repairs.

### 7. Invoices & Payments
- Manage customer invoices.
- Associate invoices with repair jobs.
- Record customer payments.
- Maintain payment history.
- Support printable payment receipts.

### 8. Customer Portal
- View registered vehicles.
- Monitor repair progress.
- Access repair information.
- View invoices and payment information.
- Access vehicle service history.

### 9. Frontend Dashboard
- Modern garage management interface.
- Administrative dashboard.
- Customer-facing dashboard.
- Mechanic-facing interface.
- Responsive layouts for different screen sizes.

## 🛠️ Technology Stack

### Backend
- Python
- Django
- Django REST Framework
- Django REST Framework Simple JWT
- MySQL
- django-filter
- DRF Spectacular (OpenAPI documentation)

### Frontend
- Modern JavaScript frontend
- HTML5
- CSS3
- REST API integration

### Deployment & Development
- Vercel (Frontend hosting)
- Git and GitHub
- Visual Studio Code
- Postman
- MySQL Workbench

## 🏗️ System Architecture

AutoCare follows a frontend-backend architecture.

```text
              CUSTOMER / ADMIN / MECHANIC
                         |
                         |
                  FRONTEND APPLICATION
                         |
                         |
                     REST APIs
                         |
                         |
                 DJANGO REST FRAMEWORK
                         |
          +--------------+--------------+
          |              |              |
      AUTHENTICATION  BUSINESS LOGIC  PERMISSIONS
          |              |              |
          +--------------+--------------+
                         |
                    MYSQL DATABASE
                         |
          +--------------+--------------+
          |              |              |
       CUSTOMERS       VEHICLES       MECHANICS
          |              |              |
          +--------------+--------------+
                         |
                  REPAIR MANAGEMENT
                         |
              +----------+----------+
              |          |          |
            PARTS     INVOICES    PAYMENTS
```

## 📂 Project Structure

```text
AutoCare/
│
├── client/
│   └── Frontend application
│
├── server/
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
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── manage.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

## 🔐 Security & Access Control

AutoCare uses authentication and permissions to protect application resources.

- JWT authentication.
- Role-based permissions.
- Customer-specific data access.
- Restricted administrative operations.
- Mechanic-specific access to assigned work.
- API validation and controlled data access.

## ⚙️ Local Development Setup

### Prerequisites

Install the following tools:

- Python
- MySQL Server
- Git
- Visual Studio Code

### 1. Clone the Repository

```bash
git clone https://github.com/irshadahmad890/AutoCare.git
cd AutoCare
```

### 2. Backend Setup

Open PowerShell:

```powershell
cd server

python -m venv venv

.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Configure your environment variables and MySQL database according to the backend settings.

Run database migrations:

```powershell
python manage.py migrate
```

Start the Django development server:

```powershell
python manage.py runserver
```

### 3. Frontend Setup

Open another terminal:

```powershell
cd client

npm install

npm run dev
```

Configure the frontend API base URL to point to your running Django backend.

**Note:** Frontend commands depend on the scripts defined in the client package.json.

## 🚀 Deployment

The frontend is hosted on Vercel.

The application uses a separate backend architecture, so the Django API and database require their own hosting and configuration.

Deployment considerations include:

- Frontend production build.
- Backend API hosting.
- Production MySQL database.
- Environment variables and secret management.
- CORS configuration.
- Secure API communication.
- Media and file storage configuration.

## 🗺️ Future Improvements

- Real-time repair progress notifications.
- Live mechanic progress updates.
- Customer approval of repair estimates.
- Advanced garage analytics.
- Automated service reminders.
- Online payment gateway integration.
- Multi-garage SaaS support.

## 👨‍💻 Developer

**Irshad Ahmad**

- GitHub: https://github.com/irshadahmad890/
- LinkedIn: https://www.linkedin.com/in/irshad-ahmad-dev/

## 📄 Project Status

**Project:** AutoCare – Garage Management SaaS

**Development:** Full-stack development

**Backend:** Core API development completed according to the current project milestone.

**Frontend:** Development and integration.

**Deployment:** Frontend preview hosted on Vercel.

---

Built to simplify garage operations through technology.
