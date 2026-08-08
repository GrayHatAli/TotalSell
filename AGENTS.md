# TotalSell Agent Guidelines

## Project Overview
TotalSell is a self-hosted back-office management platform built with:
- **Backend**: FastAPI (Python 3.12+) with PostgreSQL
- **Frontend**: SvelteKit with Tailwind CSS
- **Infrastructure**: Docker Compose for local development

## Key Directories
- `/backend` - FastAPI application
- `/frontend` - SvelteKit frontend
- `/backend/app` - Core backend application code

## Essential Commands

### Development Setup
```bash
# Setup environment
cp .env.example .env

# Start all services
docker-compose up --build

# Backend development
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

# Frontend development
cd frontend
npm install
npm run dev
```

### Testing
```bash
# Backend tests
cd backend
source .venv/bin/activate
pytest

# Frontend tests (follow SvelteKit/Vitest conventions)
cd frontend
# Check package.json for test scripts
```

### Database Management
```bash
# Apply migrations
cd backend
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"
```

## Code Organization

### Backend Structure
- `/app/main.py` - FastAPI application entry point
- `/app/config.py` - Environment configuration
- `/app/database.py` - Database connection/session
- `/app/models/` - SQLAlchemy ORM models
- `/app/schemas/` - Pydantic request/response schemas
- `/app/routers/` - API route handlers (one file per module)
- `/app/services/` - Business logic

### Frontend Structure
- `/src/routes` - SvelteKit pages and endpoints
- `/src/lib` - Shared libraries, components, utilities
- `/src/lib/i18n` - Internationalization (English/Persian)

## Key Conventions

### API Design
- Base URL: `/api/v1/`
- Authentication: `Authorization: Bearer <JWT>`
- Response format: `{ success, data, meta, error }`
- Pagination: `?page=1&page_size=20`
- Filtering: `?search=term&category_id=5`
- Sorting: `?sort_by=created_at&sort_dir=desc`

### Database Rules
- Monetary values: `NUMERIC(15, 2)` (never FLOAT)
- Timestamps: Stored UTC, displayed local
- Soft deletes: All master data uses `deleted_at`
- Immutable records: Journal entries corrected via reversals
- FIFO inventory: Implemented via `inventory_lots` table

### Backend Development
- API-first: endpoints built before UI
- Modular routers: New modules = new router files
- Transactional writes: Invoice operations use single DB transaction
- Idempotency: Financial writes should accept idempotency keys

### Frontend Development
- SvelteKit with Tailwind CSS
- RTL support built-in for Persian language
- ZXing-js for browser-based barcode scanning
- Component library: Skeleton UI
- Code formatting: Prettier (per CONTRIBUTING.md guidelines)

### Backend Code Quality
- Code formatting: Black (per CONTRIBUTING.md guidelines)
- Linting: Follows standard Python practices

## Testing Guidelines
- Backend tests located in `/tests` directory
- Run backend tests with pytest from `/backend`
- Frontend tests follow SvelteKit/Vitest conventions
- Check frontend package.json for available test scripts

## Docker Services
- Backend API: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`
- Frontend: `http://localhost:5173`
- PostgreSQL: `localhost:5432`

## Environment Setup
- Copy `.env.example` to `.env` for local development
- Default admin credentials defined in `.env`
- Never commit actual `.env` file to git

## Architecture Notes
- Financial writes (invoices, payments) must be wrapped in single DB transaction
- Invoice numbers must be allocated safely under concurrent requests
- Reports should read from canonical records, tolerate rebuilding cached summaries
- No offline financial writes until explicit sync/conflict resolution designed