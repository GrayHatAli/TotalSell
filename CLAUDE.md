# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

TotalSell is a self-hosted back-office platform: inventory, purchasing, sales invoicing, double-entry accounting, and reporting. FastAPI + PostgreSQL backend, SvelteKit + Tailwind frontend, Docker Compose for local dev. Bilingual (English/Persian) with RTL from the ground up.

Long-term architecture lives in `DESIGN.md`. `AGENTS.md` holds an earlier, partly stale version of these notes — prefer this file where they disagree.

## Commands

```bash
# Full stack (applies migrations + seeds on backend boot)
cp .env.example .env
docker-compose up --build
```

Backend:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt

pytest                                   # full suite (SQLite, see conftest.py)
pytest tests/test_invoices.py            # one file
pytest tests/test_invoices.py::test_name # one test
pytest -k "sale and not purchase"        # by expression

alembic upgrade head
alembic revision --autogenerate -m "description"
```

Frontend:
```bash
cd frontend
npm install
npm run dev
npm run check    # svelte-kit sync && svelte-check — this is the only type/lint gate
npm run build
```

There is no frontend test runner and no Python formatter/linter installed (`requirements-dev.txt` is just pytest + httpx). `AGENTS.md` mentions Black/Prettier "per CONTRIBUTING.md" — that file does not exist. Don't assume `black`, `ruff`, or `vitest` are available; check before invoking.

Services: API `:8000`, Swagger `:8000/docs`, frontend `:5173`, Postgres `:5432`.

## Backend architecture

Layering is strict and matters:

- `app/routers/*.py` — one router per domain module, each registered in `app/main.py` under `settings.api_v1_prefix`. Routers do validation, auth, pagination, and soft-delete filtering. They should not contain accounting logic.
- `app/services/*.py` — business logic. `invoice.py` (invoice posting cascade), `accounting.py` (journal entries, trial balance), `reports.py`, `auth.py`.
- `app/models/` — SQLAlchemy 2.x `Mapped[...]` declarative models. Every model must be imported in `app/models/__init__.py` or Alembic autogenerate and the test-suite `create_all` will miss it.
- `app/schemas/` — Pydantic request/response models.

### Response envelope

Every endpoint returns `ok(data, meta=...)` or `fail(code, message, details=...)` from `app/schemas/common.py`, producing `{success, data, meta, error}`. `HTTPException` and `RequestValidationError` are converted into the same envelope by handlers in `main.py`, so raising `HTTPException` is the correct way to fail — don't hand-build error responses.

List endpoints follow one shape: `?page=1&page_size=20&search=&sort_by=&sort_dir=asc`, with `meta={"page", "page_size", "total"}`.

### Auth

JWT bearer via `HTTPBearer`. Guard endpoints with `_user=Depends(get_current_user)` (underscore when the user isn't used). Access tokens 8h, refresh tokens 30d, stored hashed in `refresh_tokens` and rotated on use — refreshing revokes the old record.

### Invoice posting cascade

`create_purchase_invoice` / `create_sale_invoice` in `app/services/invoice.py` are the single write path for invoices. One call must atomically produce: the invoice + items, `InventoryMovement` rows (`IN` for purchase, `OUT` for sale, physical products only), a balanced `JournalEntry` + `JournalLine` rows, and a number from `invoice_counters`.

Journal lines are posted against hardcoded account codes seeded by `app/seed.py`: 1110 cash, 1120 bank, 1130 AR, 1140 inventory, 1150 tax receivable, 2110 AP, 2120 tax payable, 4100 revenue, 5100 COGS. `_get_account` raises if a code is missing, so changing `DEFAULT_ACCOUNTS` breaks invoice posting.

These functions currently open a *second* session bound to `db.bind` rather than using the injected session, and mix `session.begin()` with an explicit `commit()`. That is fragile and diverges from the guardrail in `DESIGN.md` §12 (single transaction, idempotency keys). If you touch this code, treat it as a known rough edge rather than a pattern to copy.

### Money and time

Monetary and quantity columns are `Numeric(15, 2)` — never `Float`. Arithmetic goes through `Decimal` with `_round`/`ROUND_HALF_UP` helpers (duplicated in `services/invoice.py`, `accounting.py`, `reports.py`). Timestamps are `DateTime(timezone=True)`, stored UTC via `datetime.now(UTC)`, formatted client-side.

### Soft deletes and immutability

Master data (products, customers, suppliers, categories) uses `deleted_at`. Every read must filter `Model.deleted_at.is_(None)`; delete endpoints set the timestamp. Journal entries are append-only — correct them with reversing entries, never by mutating or deleting lines.

### Tests

`tests/conftest.py` forces `DATABASE_URL` to SQLite and sets env vars *before* importing the app, so it must stay the first import path. An autouse fixture drops and recreates all tables and re-seeds admin + accounts per test, so tests can assume a clean DB but not shared state. Since tests run on SQLite while production is Postgres, Postgres-specific SQL will pass CI and fail in Docker.

## Frontend architecture

- `src/lib/api/*.ts` — one typed module per backend router, all going through `apiRequest` in `client.ts`. That wrapper injects the bearer token, transparently retries once after refreshing on a 401, and throws `Error(body.error.message)` — so callers only need try/catch, not envelope unwrapping. Tokens live in `localStorage` (SSR-guarded).
- `src/routes/**/+page.svelte` — pages call the API modules directly in `onMount`; there is no `+page.ts` data loading. Dashboard-style pages use `Promise.allSettled` and must tolerate partial failure (several past bug fixes were undefined-access crashes on failed branches).
- Auth gating is in `src/routes/+layout.svelte` via a reactive redirect to `/login`; there is no server-side guard.

### i18n

`src/lib/i18n/index.ts` exposes a `locale` store, a derived `dir` store, and a plain `t(key)` function. `t()` reads a module-level `currentLocale` mirror, so it is **not** reactive on its own — templates must reference `$locale` somewhere in the same reactive statement to re-render on language change (`$: label = ($locale, t('key'))`). Several commits in the history exist purely to fix this class of bug. `en.json` and `fa.json` must stay key-for-key aligned. Persian sets `dir="rtl"` on `<html>`, so prefer logical Tailwind utilities (`ms-`/`me-`, `text-start`) over `ml-`/`mr-`/`text-left`.

### Styling

Skeleton UI + Tailwind. Design tokens are defined twice and must be kept in sync: `tailwind.config.ts` (`theme.extend`) and CSS custom properties in `src/app.css` (`--color-*` → `--app-*`, including a `.dark` block). `design-system/totalsell/MASTER.md` is the source of truth for palette, Fira Sans/Fira Code typography, spacing, and shadows; per-page overrides may live in `design-system/pages/[page-name].md` and take precedence.

`vite.config.ts` deliberately forces `esbuild` for CSS minification and the `postcss` transformer, because lightningcss rejects Skeleton's `::file-selector-button:disabled`. Don't "clean up" that override.

## Conventions worth keeping

- API-first: add the endpoint and its test before the UI.
- New domain module = new file in `models/`, `schemas/`, `routers/`, plus registration in `main.py` and `models/__init__.py`, plus a matching `lib/api/` module and i18n keys in both locales.
- Migrations are checked in under `backend/alembic/versions/`; `alembic.ini` hardcodes the Docker Postgres URL, so run Alembic against a real Postgres (or override the URL), not the SQLite test DB.
