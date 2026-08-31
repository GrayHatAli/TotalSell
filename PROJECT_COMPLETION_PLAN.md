# TotalSell Project Completion Plan

**Date:** 2026-08-24  
**Purpose:** Reconcile the repository with its existing implementation plans and define the shortest safe path to a production-ready MVP.

## Executive summary

TotalSell is no longer at the Phase 0 foundation described by `README.md`. The repository contains working implementations for master data, invoices, basic accounting, reports, exports, barcode lookup/scanning, and PWA scaffolding. The existing backend suite reports **34 passing tests**, and the frontend production build completes.

The project is not complete against `DESIGN.md` or the phase plans. The most important unfinished work is financial correctness and operational hardening:

- Sales do not enforce available stock.
- Inventory is movement-based only; there are no FIFO inventory lots or cost-layer allocations.
- Payment creation is CRUD-only and does not create accounting entries or update invoice balances.
- Invoice services create a second database session, mutate the request payload, and convert monetary values through `float`.
- Invoice creation has no idempotency-key support.
- The public inventory endpoint permits direct movement creation even though the transaction plan says movements should be system-controlled.
- Frontend `npm run check` currently fails on errors in the uncommitted toast/Vite changes; it also reports accessibility warnings.
- Several plan and documentation files still describe earlier phases or claim completion without covering the remaining production requirements.

This plan treats “complete” as a reliable single-company back-office MVP. The future storefront, payment gateways, CRM, logistics, multi-user roles, and native app remain post-MVP scope.

## Evidence-based current state

Validation performed during this review:

- Backend: `PYTHONPATH=. .venv/bin/pytest -q` → **34 passed**, 2 SQLAlchemy deprecation warnings.
- Frontend: `npm run build` → **successful**, with accessibility and unused-code warnings.
- Frontend: `npm run check` → **failed** with errors in `frontend/vite.config.ts`, `frontend/src/lib/stores/toast.ts`, and `frontend/src/lib/components/ToastContainer.svelte`.
- Docker: `docker compose config --quiet` → valid configuration.
- The worktree contains uncommitted frontend/design changes. They are preserved and should be reviewed as part of Phase 0.

### Comparison with existing plans

| Planned area | Repository state | Assessment |
|---|---|---|
| Phase 0 foundation | FastAPI, SvelteKit shell, JWT auth, migrations, Docker, shared response envelope, bilingual shell | Implemented, but documentation still references a missing `MVP.md` and the frontend check gate is red |
| Phase 1 master data | Customers, suppliers, categories, tags, products, soft deletes, pagination, category parent links, product custom JSON | Implemented to the deliberately reduced scope; recursive category UI, variants, images, imports, and attribute templates remain deferred |
| Phase 2 transaction core | Bank accounts, purchase/sale invoices, payments CRUD, movements, seeded accounts, automatic invoice journals, counters | Partially implemented; stock enforcement, payment posting, idempotency, FIFO, and strict transaction behavior remain |
| Phase 3 accounting core | Manual journals, general ledger data, trial balance, P&L, balance sheet | Basic read/write flow exists; journal detail/reversal/approval/fiscal controls and contract consistency remain |
| Phase 4 reports/exports | Sales, purchases, inventory, PDF, Excel, report pages | Minimal implementation exists; CSV and the broader financial/aged/tax/cash-flow report set are absent |
| Phase 5 mobile/workflow | ZXing scanner, barcode lookup, manifest, service worker/PWA plugin, responsive shell | Scaffolding exists; mobile accessibility, authenticated downloads, offline behavior, and check-gate quality still need verification |
| BUGFIX_PLAN.md | Corrective backend work and 34-test result are recorded as complete | Useful historical record, but it overstates project completion and does not cover the gaps above |

## Completion phases

### Phase 0 — Baseline, documentation, and quality gates

**Priority:** P0  
**Goal:** Establish a trustworthy baseline before changing financial behavior.
**Status:** Completed on 2026-08-24.

Tasks:

- [x] Fix all `npm run check` errors:
  - Type the `configResolved` hook in `frontend/vite.config.ts`.
  - Align the toast type union with the supported `info` notification or remove the unsupported value.
  - Correct the invalid `{id=...}` attribute in `ToastContainer.svelte`.
- [x] Resolve the current frontend accessibility warnings for modal backdrops, close buttons, and unused toast properties/selectors.
- [x] Add a documented, reproducible test command using the project environment, with the import path handled by `backend/pytest.ini`.
- [x] Update `README.md` so it no longer claims that the current implementation follows an unavailable `MVP.md`.
- [x] Mark `DESIGN.md` roadmap checkboxes and the old `BUGFIX_PLAN.md` completion statement as historical/current status rather than future truth.
- [x] Keep `PROJECT_COMPLETION_PLAN.md` as the implementation source for the remaining MVP work.
- [x] Add CI gates for backend tests, frontend check, frontend build, migration validation, and Docker Compose configuration.

Acceptance criteria:

- [x] Backend tests pass from a clean checkout using documented commands.
- [x] `npm run check` passes with no errors and no warnings.
- [x] `npm run build` passes.
- [x] Documentation identifies the actual current phase and the remaining MVP scope.

### Phase 1 — Transaction integrity and API contract

**Priority:** P0  
**Goal:** Make every financial write deterministic, atomic, typed, and safe to retry.

Backend tasks:

- Refactor `backend/app/services/invoice.py` to use the injected SQLAlchemy session. Do not create a second session from `db.bind`, mix transaction context managers with explicit commits, or return objects from a closed session.
- Stop mutating request payloads with `pop`; copy or use typed Pydantic request models and explicit service command objects.
- Replace float-based monetary and quantity writes with `Decimal` values all the way through validation, calculation, persistence, and response serialization.
- Enforce references to active suppliers, customers, products, and bank accounts before posting.
- Validate line totals, invoice-level discounts, tax, shipping, payment method, and payment status in one canonical calculation service.
- Make invoice number allocation concurrency-safe in PostgreSQL with a unique constraint and row-lock/upsert strategy. Add a concurrent creation test against PostgreSQL, not only SQLite.
- Add idempotency keys for invoice and payment creation. A retried request must return the original result and must not duplicate inventory, journal, payment, or invoice records.
- Add a unique reference from a payment to its source request and implement payment posting as a transaction: payment record, invoice balance/status update, and balanced journal entry.
- Validate payment amount against the remaining invoice balance unless overpayments are explicitly supported.
- Decide and document the canonical report/API paths. Keep frontend helpers and backend routes aligned, including journal entry detail endpoints and pagination metadata.
- Make automatic journal entries immutable and add reversal/correction operations instead of update/delete paths.
- Wire the existing audit-log model into authentication and financial mutations.

Acceptance criteria:

- Any failure during invoice or payment posting rolls back every related record.
- Retrying the same idempotency key returns the original response without duplicate effects.
- Concurrent invoice creation produces unique numbers.
- Every posted journal entry balances exactly using `Decimal` arithmetic.
- API contracts are typed, documented in OpenAPI, and covered by integration tests.

### Phase 2 — Inventory correctness and stock workflows

**Priority:** P0  
**Goal:** Replace aggregate movement arithmetic with auditable stock and cost-layer behavior.

Tasks:

- Add the `inventory_lots` table and model described in `DESIGN.md`: source item, received quantity, remaining quantity, unit cost, batch, and optional expiry.
- On purchase, create lots and link inbound movements to the originating lot/source item.
- On sale, reserve and consume lots using FIFO; persist the allocation so COGS is reproducible later.
- Reject sales that exceed available stock for physical products. Services and digital products must bypass stock checks intentionally.
- Calculate sale-item unit cost and journal COGS from FIFO allocations, not the product’s current `cost_price`.
- Define and implement returns/refunds/credit notes as reversing workflows for inventory, payment, and accounting.
- Replace the current unrestricted inventory POST with a controlled adjustment service requiring a reason, actor, and audit record; or remove the endpoint from the MVP surface.
- Support stock adjustments and inventory counts without allowing arbitrary historical references.
- Update product inventory and inventory reports to show on-hand quantity, valuation, lots, low stock, and movement traceability without N+1 queries.
- Add tests for partial lot consumption, multiple cost layers, insufficient stock, returns, adjustments, and rollback.

Acceptance criteria:

- Stock on hand equals the sum of lot balances and is traceable to source transactions.
- Every sale has a deterministic FIFO COGS result.
- Negative stock cannot be created through any public API.
- Inventory reports and product detail agree with the ledger and lot state.

### Phase 3 — Accounting completeness and reporting contracts

**Priority:** P1  
**Goal:** Turn the current basic accounting/reporting implementation into a dependable management layer.

Tasks:

- Add journal entry detail retrieval with nested lines, account validation, date filtering, and consistent pagination.
- Add reversal-entry workflows and prevent mutation/deletion of posted entries.
- Add opening balances and a documented retained-earnings treatment so the balance sheet remains meaningful across periods.
- Add account hierarchy/parent support and safe chart-of-accounts administration, including protection for system account codes used by invoice posting.
- Expand reports to match the design scope: cash-flow summary, tax/VAT summary, receivables/payables aging, top products, sales by category, customer purchase history, stock valuation, and movement history.
- Add CSV export in addition to PDF and Excel where specified.
- Make report date boundaries timezone-safe and consistent between frontend, API, and database.
- Move expensive report aggregation to grouped SQL queries and add indexes based on query plans; avoid one query per product.
- Add report tests with known journal, payment, lot, return, and opening-balance fixtures.

Acceptance criteria:

- Trial balance balances for every tested period.
- P&L, balance sheet, inventory valuation, and customer/supplier balances reconcile to canonical transactions.
- Exported files contain the same values as the JSON report response.
- Reports remain correct after reversals, payments, returns, and partial lot consumption.

### Phase 4 — Frontend productization and workflow UX

**Priority:** P1  
**Goal:** Make all completed backend workflows usable, accessible, localized, and safe in the browser.

Tasks:

- Finish the Phase 0 frontend fixes and keep `svelte-check` as a required gate.
- Replace duplicated invoice, modal, table, loading, empty-state, and error patterns with shared components where behavior is identical.
- Complete bilingual coverage: remove hardcoded English labels from invoice, payment, bank-account, report, and scanner flows; keep `en.json` and `fa.json` key-for-key aligned.
- Audit RTL layout using logical spacing/alignment utilities and verify the design-system tokens are consistent between Tailwind and CSS variables.
- Add invoice detail views with printable/PDF actions, payment history, stock effects, and journal references.
- Make report/PDF/Excel downloads use the authenticated API client or a token-safe download mechanism; direct unauthenticated `window.open`/anchor URLs must not be relied on.
- Improve invoice forms with searchable product/customer/supplier selection, per-line validation, stock feedback, totals preview, duplicate-submit protection, and clear transaction errors.
- Make barcode scanning resilient: permission denial, no camera, unsupported device, repeated scans, unmatched code, and manual fallback.
- Complete mobile checks at 375px, 768px, 1024px, and desktop widths, including tables, modals, sidebar, camera view, and touch targets.
- Add component/unit tests for API helpers and critical form calculations; add browser smoke tests for login, master data, invoice posting, payment, reports, and barcode fallback.

Acceptance criteria:

- `npm run check` and `npm run build` pass.
- All primary workflows are available in English and Persian with correct RTL behavior.
- Authenticated users can view/download protected reports and invoices.
- Critical workflows pass browser smoke tests on desktop and mobile viewport sizes.

### Phase 5 — Production hardening and release readiness

**Priority:** P1  
**Goal:** Verify the application under its intended PostgreSQL/Docker runtime and prepare a safe release.

Tasks:

- Run migrations and the full integration suite against PostgreSQL 16 in Docker; keep SQLite only for fast unit tests where behavior is portable.
- Add migration upgrade tests from a fresh database and from a representative existing database.
- Validate production settings: no development JWT/admin defaults, explicit CORS origins, secure deployment configuration, HTTPS guidance, and secret rotation.
- Add readiness/liveness checks for API and database, structured logs, request correlation, and actionable startup failures.
- Add backup/restore documentation and a release rollback procedure for database migrations.
- Add rate limiting for login and protected file/PDF endpoints, and review authorization on every route.
- Verify audit logs cover login, master-data changes, invoice/payment posting, stock adjustments, reversals, and administrative actions.
- Define PWA behavior precisely: cached shell only, no offline financial writes, visible offline state, and login redirect behavior when API access is unavailable.
- Add a release checklist covering dependency lockfiles, database migrations, Docker images, accessibility, security, and documentation.

Acceptance criteria:

- A clean `docker compose up --build` creates a usable PostgreSQL-backed installation and applies migrations once.
- Postgres integration, concurrency, idempotency, and browser smoke suites pass.
- Backup/restore and rollback procedures have been exercised at least once.
- No known P0/P1 correctness, security, or release-blocking issue remains.

## Post-MVP roadmap

Only begin these after Phases 0–5 are accepted:

1. **Operations enhancement:** multi-user roles, purchase orders, supplier price lists, advanced lot/expiry workflows, notifications, imports, dashboards, and Telegram integration.
2. **Customer-facing:** storefront, payment gateways, customer portal, CRM, logistics, and customer notifications.
3. **Open-source maturity:** Playwright coverage, published images, one-click VPS deployment, English/Persian contributor documentation, and a demo instance.

## Dependency order

```text
Phase 0 quality gates
        ↓
Phase 1 transaction integrity ─────┐
        ↓                           │
Phase 2 inventory/FIFO              │
        ↓                           │
Phase 3 accounting and reports     │
        ↓                           │
Phase 4 frontend workflows ────────┘
        ↓
Phase 5 PostgreSQL/Docker/release verification
```

Phase 1 must precede FIFO and report expansion because inventory, accounting, and payment correctness depend on a single reliable transaction boundary. Phase 4 can proceed in parallel with the backend work after the API contracts are frozen, but protected downloads and invoice UX should wait for the final API contract.

## Definition of MVP complete

TotalSell can be called MVP-complete when all of the following are true:

- Master data, purchasing, sales, payments, inventory, accounting, and reports work end to end.
- Financial writes are atomic, idempotent, auditable, and safe under concurrent PostgreSQL requests.
- Physical inventory uses FIFO lots, blocks negative stock, and reconciles to COGS and valuation reports.
- Corrections use documented reversal/return workflows; posted financial records are immutable.
- Frontend check/build gates and critical browser workflows pass in both locales.
- Docker/PostgreSQL setup, migrations, backups, security settings, and release procedures are verified.
- Remaining deferred features are explicitly listed as post-MVP rather than silently treated as complete.
