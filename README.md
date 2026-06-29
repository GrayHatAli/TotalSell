# TotalSell

TotalSell is a self-hosted back-office management platform for inventory, purchasing, sales invoicing, accounting, and reporting.

This repository is being rebuilt as a FastAPI, SvelteKit, and PostgreSQL application. The current implementation follows the Phase 0 foundation described in `MVP.md`.

## Quick Start

```bash
cp .env.example .env
docker-compose up --build
```

Services:

- Backend API: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`
- Frontend: `http://localhost:5173`
- PostgreSQL: `localhost:5432`

Default local admin credentials are defined in `.env`.

## Local Backend Tests

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```

## Language Support

The frontend foundation supports English and Persian from the start. Locale, text direction, and translations live under `frontend/src/lib/i18n`.

## Project Documents

- `DESIGN.md` - long-term architecture and module design
- `MVP.md` - current Phase 0 implementation scope

