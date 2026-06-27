# TotalSell MVP - Phase 0 Foundation

## Purpose

The first MVP step is to create a working foundation for the Python/SvelteKit rebuild. It should prove the project can run locally, persist data, authenticate an admin user, expose documented APIs, and render a responsive application shell.

This phase intentionally avoids invoice posting, inventory valuation, accounting reports, barcode scanning, PDF generation, and Excel export. Those features depend on a stable foundation and belong in later phases.

## Scope

- FastAPI backend scaffold
- SvelteKit frontend scaffold
- PostgreSQL database through Docker Compose
- SQLAlchemy 2.x models and Alembic migrations
- JWT login for a single admin user
- Shared API response envelope
- Pagination, filtering, sorting, and error conventions
- Health check endpoint
- Responsive authenticated layout shell
- Basic automated tests for backend startup, auth, and health checks

## Non-Goals

- Customer, supplier, product, invoice, inventory, or accounting CRUD
- Multi-user roles and permissions
- Offline financial writes
- Barcode scanning
- Report generation
- Production deployment automation

## Backend Deliverables

- `backend/app/main.py` creates the FastAPI application.
- `backend/app/config.py` loads settings from environment variables.
- `backend/app/database.py` configures SQLAlchemy sessions.
- `backend/app/models/user.py` defines the first admin user model.
- `backend/app/schemas/` contains auth and shared response schemas.
- `backend/app/routers/auth.py` exposes login and token refresh endpoints.
- `backend/app/routers/health.py` exposes health and database readiness checks.
- `backend/alembic/` contains the initial migration.
- `backend/tests/` includes pytest coverage for health checks and auth.

## Frontend Deliverables

- SvelteKit app scaffold under `frontend/`.
- Tailwind CSS and Skeleton UI installed and configured.
- Login page wired to the backend auth endpoint.
- Authenticated layout shell with navigation placeholders for future modules.
- API client wrapper that applies the response envelope and token handling.
- Mobile-first responsive layout with RTL-ready styling.

## Docker Deliverables

- `docker-compose.yml` starts PostgreSQL, backend, and frontend.
- `.env.example` documents all required local settings.
- Backend and frontend Dockerfiles support local development.
- `README.md` quick start can bring the stack up with one command.

## API Contract

```http
GET  /api/v1/health
GET  /api/v1/health/db
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
GET  /api/v1/auth/me
```

All JSON responses use the shared envelope:

```json
{
  "success": true,
  "data": {},
  "meta": null,
  "error": null
}
```

## Data Model

Minimum tables:

- `users`: admin identity, password hash, active flag, timestamps
- `refresh_tokens`: hashed token, user reference, expiry, revocation timestamp
- `audit_log`: initial administrative/security events

## Acceptance Criteria

- `docker-compose up --build` starts the full stack.
- Backend docs are available at `/docs`.
- Alembic can create and upgrade the database from scratch.
- An admin user can log in and access `/api/v1/auth/me`.
- Invalid credentials return a consistent error envelope.
- The frontend login page works against the local backend.
- The authenticated shell renders correctly on desktop and mobile widths.
- Backend tests pass locally.

## Exit Criteria

Phase 0 is complete when a new contributor can clone the repository, copy `.env.example`, start the stack, log in as the seeded admin user, and see a responsive authenticated shell backed by a working PostgreSQL database.
