# Workforce Intelligence AI

Workforce Intelligence AI is a FastAPI + React + PostgreSQL project for workforce planning, department management, predictive analytics, and HR decision support. The codebase is structured around a real backend API and a data-driven frontend, with the main verified baseline focused on employee management, department management, workforce history, dashboard analytics, and explainable forecasting/recommendation logic driven by actual database records.

## Verified working baseline

The repository currently includes a working backend and frontend baseline that has been checked in the available environment.

- Backend: FastAPI app boots successfully using the backend project root and `PYTHONPATH=.`.
- Database: PostgreSQL runs via Docker Compose and the health endpoint reports `database: connected` when the app is running.
- Core tests: `PYTHONPATH=. pytest -q` passes for the backend API suite.
- Frontend: Vite build completes successfully after installing frontend dependencies.

## Project architecture

- Frontend: React + Vite + Axios + React Router + Recharts
- Backend: Python + FastAPI + SQLAlchemy + Pydantic
- Database: PostgreSQL 15
- ML/analytics: Pandas + NumPy + scikit-learn + joblib
- API docs: FastAPI OpenAPI at `/docs`

## Repository layout

- `backend/` — FastAPI application, SQLAlchemy models, services, tests, and configuration
- `frontend/` — React frontend and UI pages
- `docker-compose.yml` — PostgreSQL container definition
- `ml/` — saved models and forecasting-related outputs
- `data/` — sample and imported datasets

## Prerequisites

- Python 3.11+ or 3.12+
- Node.js 18+ and npm
- Docker and Docker Compose for PostgreSQL
- PostgreSQL 15 service (via Docker Compose in this repo)

## Environment configuration

### Backend

Create or update `backend/.env` from `backend/.env.example`.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/workforce_db
SECRET_KEY=change_this_secret
ENVIRONMENT=development
```

The backend settings are loaded with `pydantic-settings` from `backend/.env` using the project root context.

### Frontend

Create `frontend/.env` from `frontend/.env.example`.

Example:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## PostgreSQL setup

From the repository root:

```bash
docker compose up -d db
```

This starts a PostgreSQL container named `workforce-postgres` and exposes port `5432`.

Database details from `docker-compose.yml`:

- Database: `workforce_db`
- Username: `username`
- Password: `password`

These are example development credentials and should only be used in the local development environment.

## Backend installation and startup

```bash
cd workforce-planning-forecasting/backend
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
PYTHONPATH=. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

To initialize the database schema from the app metadata:

```bash
cd workforce-planning-forecasting/backend
. .venv/bin/activate
PYTHONPATH=. python - <<'PY'
from app.db.database import create_db_and_tables
create_db_and_tables()
PY
```

To load sample development data:

```bash
cd workforce-planning-forecasting/backend
. .venv/bin/activate
PYTHONPATH=. python scripts/seed_database.py
```

## Frontend installation and startup

```bash
cd workforce-planning-forecasting/frontend
npm install
cp .env.example .env
npm run dev -- --host 0.0.0.0
```

The frontend listens on the default Vite port `5173`.

## Docker Compose startup

From the repository root:

```bash
docker compose up -d
```

This repo currently provides the database service only; the backend and frontend are started locally with their respective commands above.

## API documentation

Once the backend is running, the FastAPI Swagger UI is available at:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Core API features

The backend exposes the following main routes:

- `GET /health` — backend and database health
- `GET /api/departments` — list departments
- `POST /api/departments` — create department
- `PUT /api/departments/{department_id}` — update department
- `DELETE /api/departments/{department_id}` — delete department
- `GET /api/departments/{department_id}/employees` — department employees
- `GET /api/employees` — paginated employee listing with filters
- `POST /api/employees` — create employee
- `PUT /api/employees/{employee_id}` — update employee
- `DELETE /api/employees/{employee_id}` — delete employee
- `GET /api/workforce-history` — workforce history records
- `POST /api/workforce-history` — create history entry
- `POST /api/workforce-history/import` — CSV import
- `GET /api/analytics/summary` — dashboard summary
- `GET /api/workforce-gap` — gap analysis
- `GET /api/attrition` — attrition overview
- `GET /api/recommendations` — explainable HR recommendations
- `POST /api/forecast` — generate forecast
- `GET /api/forecast` — list forecast records
- `GET /api/forecast/{department_id}` — department forecast

## Employee, department, and workforce-history workflows

- Employee management: create, update, delete, search, filter, and import CSV data through the API and frontend.
- Department management: create, edit, list, and review employee counts with safe delete behavior when a department is still in use.
- Workforce history: supports monthly workforce snapshots with validation, duplicate prevention, and CSV import checks.
- Analytics: dashboard summary and department-level workforce distributions are driven by actual employee and department records.

## Running tests

Backend:

```bash
cd workforce-planning-forecasting/backend
. .venv/bin/activate
PYTHONPATH=. pytest -q
```

Frontend build check:

```bash
cd workforce-planning-forecasting/frontend
npm install
npm run build
```

## Known limitations and non-production assumptions

- Forecasting is implemented as a lightweight linear-regression workflow based on workforce-history data and should be treated as decision support rather than production-grade forecasting.
- Workforce gap analysis is based on the latest forecast versus current headcount; it is only meaningful when valid historical data exists.
- Attrition analysis is a heuristic summary based on current employment status, satisfaction, and performance indicators. It is not a validated individual risk model.
- Recommendations are explainable rule-based suggestions and must be reviewed by HR professionals.
- The app does not include a full multi-user authentication and authorization system; this remains a design gap if the project is intended for production use with protected employee data.
- PostgreSQL is a local development dependency in this repository and should be configured securely before real organizational data is used.

## Troubleshooting

### Backend import errors

Use:

```bash
PYTHONPATH=. pytest -q
```

When running from the backend project root. Do not run tests from outside the backend root without setting the Python path.

### Database connection errors

Check:

- Docker container is running: `docker compose ps`
- `.env` contains the correct `DATABASE_URL`
- PostgreSQL port `5432` is open
- The `workforce_db` database exists

### Frontend cannot reach backend

Ensure:

- The backend is running at `http://127.0.0.1:8000`
- `frontend/.env` contains correct `VITE_API_BASE_URL`
- CORS settings allow the frontend origin

## Current status

The verified baseline is stable enough for local development and demonstration:

- backend health and connectivity are working
- employee and department APIs are working
- workforce-history API routes and CSV validation are in place
- dashboard analytics are connected to real database records
- forecasting, gap analysis, and recommendation logic are implemented with explainable, data-driven assumptions but are not production-validated ML systems

