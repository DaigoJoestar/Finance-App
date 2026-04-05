# Finance Dashboard Backend

![Python](https://img.shields.io/badge/python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-2.3-black)
![JWT](https://img.shields.io/badge/JWT-auth-orange)
![Docker](https://img.shields.io/badge/Docker-ready-blue)

> Flask API with role‑based access control, financial record management, and real‑time dashboard analytics.

---

##  Table of Contents

- [Features](#features)
- [Architecture (MVC)](#architecture-mvc)
- [Data Model](#data-model)
- [Quick Start with Docker](#quick-start-with-docker)
- [API Endpoints](#api-endpoints)
- [Role‑Based Access](#role-based-access)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)

---

##  Features

| Area | Capabilities |
|------|--------------|
| **User & Role Management** | Create, update, delete users; assign roles (`viewer`/`analyst`/`admin`); activate/deactivate |
| **Financial Records** | CRUD operations, pagination, filtering (by date, category, type) |
| **Dashboard Summaries** | Total income, total expenses, net balance, category totals, recent activity, monthly trends |
| **Access Control** | `@role_required` decorator enforces permissions on every endpoint |
| **Validation** | Marshmallow schemas + meaningful error responses |
| **Persistence** | SQLite (default) – switchable to PostgreSQL/MySQL via `DATABASE_URL` |
| **Containerization** | Docker + Docker Compose ready |
| **Migrations** | Flask‑Migrate for schema versioning |
| **CLI Commands** | `flask seed` (admin user) |

---

##  Architecture (MVC)

The project follows a clean **Model‑View‑Controller** separation:

| Layer | Responsibility | Files |
|-------|----------------|-------|
| **Model** | Database schema, relationships, serialization | `models.py` |
| **View** | JSON response formatting (inside models/controllers) | `to_dict()` methods |
| **Controller** | Validation, orchestration, error handling | `controllers/*.py` |
| **Service** | Business logic, database operations | `services/*.py` |
| **Route** | Endpoint definitions, request parsing | `routes/*.py` |

This makes the code testable, maintainable, and reusable.

---

##  Data Model

### `User`
| Column | Type | Notes |
|--------|------|-------|
| `id` | Integer (PK) | Auto‑increment |
| `username` | String(80) | Unique |
| `email` | String(120) | Unique |
| `password_hash` | String(128) | Hashed with Werkzeug |
| `role` | String(20) | `viewer`, `analyst`, `admin` (default: `viewer`) |
| `active` | Boolean | Can the user log in? |

### `FinancialRecord`
| Column | Type | Notes |
|--------|------|-------|
| `id` | Integer (PK) | Auto‑increment |
| `amount` | Float | Positive number |
| `type` | String(10) | `income` or `expense` |
| `category` | String(50) | e.g., "Groceries", "Salary" |
| `date` | Date | Default: today |
| `description` | Text | Optional |
| `user_id` | Integer (FK) | References `users.id` |

---

##  Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/DaigoJoestar/finance_dashboard.git
cd finance_dashboard

# Build and start the container
docker-compose up -d --build

# Initialize database and seed admin
docker exec -it finance_application-web-1 flask db upgrade
docker exec -it finance_application-web-1 flask seed
```
## API Endpoints
Authentication
| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| POST	| /api/auth/login	| {username, password} |	Returns JWT token|

Users (admin only)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST	| /api/users |	Create user |
| GET |	/api/users	| List users (paginated) |
| GET |	/api/users/<id> |	Get user by ID |
| PUT	|/api/users/<id>	| Update user |
| DELETE	| /api/users/<id> |	Delete user |

Financial Records
| Method | Endpoint | Permissions | Description |
|--------|----------|-------------|-------------|
| POST	| /api/records |	admin	| Create record |
| GET	| /api/records	| viewer+	| List (filters + pagination) |
| GET	| /api/records/<id>	| viewer+	| Get single record |
| PUT |	/api/records/<id> |	admin	| Update record |
| DELETE |	/api/records/<id> |	admin	| Hard delete |

Filters for GET /api/records: type, category, date_from, date_to, page, per_page

---

Dashboard (analyst+admin only)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET	| /api/dashboard/summary	| Total income, expenses, net balance |
| GET	| /api/dashboard/by-category	| Income & expense per category |
| GET |	/api/dashboard/recent |	Last 5 transactions |
| GET |	/api/dashboard/trends	| Monthly trends (income/expense/net) |

All dashboard endpoints accept an optional ?year=YYYY filter (except recent and trends).
---
<a id="role-based-access"></a>
##  Role‑Based Access
| Role | Permissions |
|--------|-----------|
| `viewer` |	View financial records (GET /api/records) |
| `analyst`	| View records + all dashboard summaries |
| `admin` |	Full CRUD on records + user management |

Enforced via @role_required('role') decorator.
---
##  Environment Variables
Create a .env file (ignored by Git) for secrets:


Variable	Default	Description
JWT_SECRET_KEY	jwt-secret	Used to sign JWT tokens (override in production)
SECRET_KEY	dev-secret-key	Flask session secret
DATABASE_URL	sqlite:///finance.db	SQLAlchemy connection string

---
##  Project Structure
```text
finance_dashboard/
├── app.py                 # App factory & CLI commands
├── config.py              # Config (reads from env)
├── models.py              # SQLAlchemy models
├── schemas.py             # Marshmallow validation
├── decorators.py          # @role_required
├── extensions.py          # db, migrate, jwt instances
├── controllers/           # Orchestration & validation
├── services/              # Business logic & DB ops
├── routes/                # Endpoint definitions
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```
