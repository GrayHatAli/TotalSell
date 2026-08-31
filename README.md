# TotalSell

TotalSell is a self-hosted back-office management platform for inventory, purchasing, sales invoicing, accounting, and reporting.

This repository is being rebuilt as a FastAPI, SvelteKit, and PostgreSQL application. The codebase is past the original foundation work and now contains master data, transactions, accounting, reports, exports, barcode scanning, and PWA scaffolding.

The remaining MVP work is tracked in `PROJECT_COMPLETION_PLAN.md`. The most important unfinished areas are financial transaction integrity, FIFO inventory lots, payment posting, reporting completeness, and production hardening.

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
pytest -q
```

If the local virtual environment already exists, use:

```bash
cd backend
PYTHONPATH=. .venv/bin/pytest -q
```

## Local Frontend Checks

```bash
cd frontend
npm install
npm run check
npm run build
```

## Language Support

The frontend foundation supports English and Persian from the start. Locale, text direction, and translations live under `frontend/src/lib/i18n`.

## Project Documents

- `DESIGN.md` - long-term architecture and module design
- `PROJECT_COMPLETION_PLAN.md` - current implementation plan for completing the MVP
- `BUGFIX_PLAN.md` - historical bugfix/refactoring record, not the current project completion plan
