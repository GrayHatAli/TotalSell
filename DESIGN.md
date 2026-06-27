# TotalSell - Design Document

> **Version:** 0.1.0 (Draft)
> **Status:** Planning Phase
> **Last Updated:** 2026-06-27
> **License:** MIT (intended for open-source release)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Goals & Non-Goals](#2-goals--non-goals)
3. [System Architecture](#3-system-architecture)
4. [Tech Stack](#4-tech-stack)
5. [Core Module Specifications](#5-core-module-specifications)
6. [Future Module Specifications](#6-future-module-specifications)
7. [Database Design](#7-database-design)
8. [API Design Principles](#8-api-design-principles)
9. [Barcode Scanner Integration](#9-barcode-scanner-integration)
10. [Accounting Engine](#10-accounting-engine)
11. [Reporting System](#11-reporting-system)
12. [Implementation Guardrails](#12-implementation-guardrails)
13. [Security Considerations](#13-security-considerations)
14. [Project Structure](#14-project-structure)
15. [Development Roadmap](#15-development-roadmap)
16. [Open Source Guidelines](#16-open-source-guidelines)

---

## 1. Project Overview

**TotalSell** is a comprehensive, self-hosted back-office management platform suitable for any business that sells products or services. It handles the full internal operations cycle: inventory, purchasing, sales invoicing, double-entry accounting, supplier and customer management, and advanced reporting.

The application is built as a **responsive web app (PWA)** that runs beautifully on desktop browsers, Android, and iOS without requiring a native app installation. A barcode scanner works directly through the device camera or laptop webcam inside the browser.

Although initially built for personal use, the architecture is designed to be **modular and extensible** so that future modules (payment gateways, online storefront, CRM, logistics) can be added without rewriting the core.

This design is a Python/SvelteKit rebuild plan. Any existing legacy implementation should be treated as a reference for business rules only unless a migration plan explicitly keeps part of it.

---

## 2. Goals & Non-Goals

### Goals

- Full back-office control for any single-owner business selling products or services
- Double-entry accounting with automatic journal entry creation per invoice
- Real-time inventory tracking linked to every purchase/sale
- Barcode scanning directly in the browser (camera + webcam)
- Responsive UI that works excellently on mobile (RTL support)
- Clean, modular codebase ready for open-source publication
- API-first design to support future frontends and integrations

### Non-Goals (Phase 1)

- No customer-facing storefront or online shop
- No payment gateway integration
- No shipping / logistics management
- No multi-user roles beyond admin (single owner)
- No native mobile app (PWA covers mobile needs)

---

## 3. System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Client Layer (Browser / PWA)            │
│         SvelteKit + Tailwind CSS + ZXing-js              │
│              RTL · Responsive · PWA-capable              │
└────────────────────────┬────────────────────────────────┘
                         │  REST API (JSON)
                         │  JWT Authentication
┌────────────────────────▼────────────────────────────────┐
│                  Backend Layer                           │
│                FastAPI (Python 3.12+)                    │
│      Modular Routers · Pydantic Schemas · Async          │
│         Pandas (reports) · WeasyPrint (PDF)              │
│              openpyxl (Excel export)                     │
└────────────────────────┬────────────────────────────────┘
                         │  SQLAlchemy ORM
                         │  Alembic Migrations
┌────────────────────────▼────────────────────────────────┐
│                  Data Layer                              │
│                 PostgreSQL 16+                           │
│          ACID · Transactions · Full-text search          │
└─────────────────────────────────────────────────────────┘

Supporting Tools:
  Docker Compose   — one-command local setup
  Alembic          — database schema versioning
  WeasyPrint       — invoice PDF generation
  openpyxl         — Excel report export
  ZXing-js         — browser-based barcode scanning
```

### Core Design Principles

**API-First:** Every feature is exposed through a REST API endpoint before any UI is built. This means future frontends (mobile app, Telegram bot, online store) can consume the same API with zero backend changes.

**Modular Routers:** The FastAPI backend is split into independent router modules. Adding a new module (e.g., logistics) means creating a new router file and registering it — no changes to existing code.

**Transactional Inventory & Accounting:** Every invoice creation triggers an automatic cascade:
1. Journal entry (double-entry) is created
2. Inventory quantity is updated
3. Reports are invalidated/refreshed

This cascade is handled at the service layer, not the API layer. Invoice creation, journal entry creation, inventory movement creation, and payment recording must run inside one database transaction so they commit or roll back together.

**PWA Scope:** Phase 1 supports installability, responsive layouts, and offline access to already-loaded static assets. Offline financial writes are out of scope until a durable sync and conflict-resolution model is designed.

---

## 4. Tech Stack

| Layer | Technology | Reason |
|---|---|---|
| Frontend framework | SvelteKit | Simpler than React, minimal boilerplate, excellent mobile perf |
| CSS framework | Tailwind CSS | Utility-first, RTL support, responsive by default |
| UI components | Skeleton UI | Prebuilt accessible components for Svelte/Tailwind |
| Barcode scanning | ZXing-js | Works in browser, no app install, camera + webcam |
| Backend framework | FastAPI (Python) | Async, auto Swagger docs, familiar Python ecosystem |
| ORM | SQLAlchemy 2.x | Mature, async support, works perfectly with FastAPI |
| DB migrations | Alembic | Git-like versioning for database schema changes |
| Database | PostgreSQL 16+ | ACID compliance, essential for financial data |
| PDF generation | WeasyPrint | HTML/CSS → PDF, ideal for invoice templates |
| Excel export | openpyxl | Lightweight Excel file generation in Python |
| Report processing | Pandas | Powerful data aggregation for reports |
| Auth | JWT (python-jose) | Stateless, standard, easy to extend |
| Containerization | Docker + Docker Compose | One-command setup for any machine |

---

## 5. Core Module Specifications

### 5.1 Customer Management

Manages the business's customer base.

**Fields:**
- Full name, phone number, email (optional)
- National ID (optional)
- Customer group (e.g., Regular, VIP, Wholesale)
- Credit limit (for deferred payment)
- Billing address(es)
- Notes / tags
- Account balance (derived from invoices, payments, and journal postings)
- Created at, updated at

**Features:**
- Search by name, phone, or ID
- Customer statement (list of all invoices + payments)
- Outstanding balance view
- Customer grouping for bulk discounts

---

### 5.2 Supplier Management

Manages product/service suppliers and purchase conditions.

**Fields:**
- Company name, contact person, phone, email
- National company ID / tax ID
- Bank account details (for payment tracking)
- Payment terms (e.g., net 30 days)
- Default currency
- Notes / tags
- Account balance (derived from purchase invoices, payments, and journal postings)

**Features:**
- Supplier statement (purchase history)
- Outstanding payables per supplier
- Link products to their primary supplier

---

### 5.3 Product & Service Management

Manages the catalog of physical products, digital goods, and services.

**Fields:**
- Product/service name
- SKU (auto-generated or manual)
- Barcode (EAN-13 / QR — for physical products)
- Category (hierarchical)
- Tags (multi-select)
- Product type: Physical / Digital / Service
- Unit of measure (piece, kg, hour, box, license, etc.)
- Cost price (last purchase price)
- Sale price
- Minimum stock alert threshold (for physical products)
- Product images (up to 5)
- Custom attributes (flexible key-value fields per category)
- Active / inactive status

**Features:**
- Advanced search and filter by category, tag, type, and custom attributes
- Product variants (e.g., same item in different sizes or configurations)
- Bulk price update
- Import products via Excel template
- Barcode label printing (PDF)

---

### 5.4 Category & Tag Management

Organizes the product and service catalog.

**Category structure:**
- Hierarchical tree (unlimited depth, e.g., Electronics → Accessories → Cables)
- Each category can define its own custom attribute fields (visible only for products in that category)
- Category image

**Tag structure:**
- Flat list of tags (e.g., "bestseller", "on-sale", "discontinued", "imported")
- Multiple tags per product/service
- Filter catalog by tag

---

### 5.5 Bank Account Management

Tracks money across multiple bank accounts and cash sources.

**Account types:**
- Bank account (with IBAN, account number, bank name)
- Cash register
- Digital wallet / payment terminal

**Features:**
- Current balance (derived from reconciled transaction and payment postings)
- Manual transaction entry (deposit / withdrawal)
- Bank reconciliation (mark transactions as reconciled)
- Transfer between accounts
- Transaction history with search and filter

---

### 5.6 Purchase Invoice

Records purchases from suppliers and automatically updates inventory and accounting.

**Invoice fields:**
- Invoice number (auto-generated)
- Date
- Supplier (linked)
- Reference number (supplier's invoice number)
- Line items:
  - Product / service (linked, with barcode scan support)
  - Quantity
  - Unit cost price
  - Discount %
  - Tax % (VAT)
  - Line total
- Invoice-level discount
- Shipping / handling cost
- Grand total
- Payment method (cash / bank / credit)
- Payment status (paid / partial / unpaid)
- Notes
- Attachments (e.g., photo or scan of supplier invoice)

**Automatic cascade on save:**
1. Inventory: quantity increases for each physical product line item
2. Accounting: journal entry created automatically:
   - DR Inventory (asset) — per line item cost
   - DR Tax Receivable (if VAT)
   - CR Accounts Payable / Bank / Cash — grand total
3. Supplier balance becomes visible through derived payable/payment totals

**Features:**
- Barcode scanner to add products to line items
- Partial payment tracking
- Convert to return / credit note
- PDF export of invoice
- Duplicate invoice

---

### 5.7 Sale Invoice

Records sales to customers with the same automatic cascade.

**Invoice fields:**
- Invoice number (auto-generated, separate series from purchase)
- Date
- Customer (linked, or walk-in)
- Line items:
  - Product / service (linked, with barcode scan support)
  - Quantity
  - Unit sale price (editable, pre-filled from product)
  - Discount %
  - Tax % (VAT)
  - Line total
- Invoice-level discount
- Grand total
- Payment method
- Payment status
- Notes

**Automatic cascade on save:**
1. Inventory: quantity decreases for each physical product line item
2. Accounting: journal entry created automatically:
   - DR Accounts Receivable / Bank / Cash — grand total
   - CR Sales Revenue — subtotal
   - CR Tax Payable (if VAT)
   - DR Cost of Goods Sold — inventory cost
   - CR Inventory — inventory cost
3. Customer balance becomes visible through derived receivable/payment totals

**Features:**
- Barcode scanner to add products
- Stock availability check before saving
- PDF invoice generation (printable, shareable)
- Share invoice link (WhatsApp / email)
- Return / refund flow

---

### 5.8 Double-Entry Accounting Engine

Handles the financial accounting layer automatically.

**Chart of Accounts (default structure):**

```
1000  Assets
  1100  Current Assets
    1110  Cash
    1120  Bank Accounts
    1130  Accounts Receivable
    1140  Inventory
    1150  Tax Receivable
2000  Liabilities
  2100  Current Liabilities
    2110  Accounts Payable
    2120  Tax Payable
3000  Equity
  3100  Owner's Equity
  3200  Retained Earnings
4000  Revenue
  4100  Sales Revenue
5000  Expenses
  5100  Cost of Goods Sold
  5200  Operating Expenses
    5210  Rent
    5220  Salaries
    5230  Shipping Expense
    5240  Miscellaneous
```

The chart of accounts is fully customizable — users can add, rename, or restructure accounts to match their business type and local accounting standards.

**Features:**
- Auto journal entry per invoice (purchase and sale)
- Manual journal entry for other transactions (rent, salary, utilities, etc.)
- General ledger view per account
- Trial balance report
- Journal entry approval (optional flag)
- Fiscal year management

---

### 5.9 Inventory Management

Tracks stock levels in real-time, linked to every invoice.

**Features:**
- Current stock level per product
- Stock movement history (every increase/decrease with source reference)
- Low stock alerts (in-app notification)
- Stock valuation (FIFO method, backed by cost layers)
- Batch / lot tracking with optional expiry dates
- Manual stock adjustment (with reason: damaged, lost, counted, returned)
- Inventory count sheet (export to Excel, import corrections)

---

### 5.10 Reporting System

Advanced reports across all modules.

**Financial Reports:**
- Profit & Loss Statement (Income Statement) — daily / monthly / yearly
- Balance Sheet — as of any date
- Trial Balance
- Cash Flow Summary
- Tax Summary (VAT collected vs paid)

**Sales Reports:**
- Sales by period (daily / weekly / monthly)
- Best-selling products and services (by quantity and revenue)
- Sales by category
- Customer purchase history
- Outstanding receivables (aged)

**Purchase Reports:**
- Purchases by period
- Purchases by supplier
- Outstanding payables (aged)

**Inventory Reports:**
- Current stock levels (all products)
- Low stock alert list
- Stock valuation report
- Stock movement history

**Export formats:** PDF, Excel (.xlsx), CSV

---

## 6. Future Module Specifications

These modules are **not built in Phase 1**. Phase 1 keeps stable extension points for them, but does not prebuild unused schemas unless the table is required by the active feature set.

| Module | Description | API Namespace |
|---|---|---|
| Online Storefront | Customer-facing product catalog and order placement | `/api/v1/storefront/` |
| Payment Gateway | Integration with online payment providers | `/api/v1/payments/` |
| CRM & Support | Customer ticketing, follow-up, loyalty points | `/api/v1/crm/` |
| Logistics | Shipping methods, tracking, courier integration | `/api/v1/logistics/` |
| Mobile App | Capacitor wrapper of the PWA for app store distribution | — |
| Multi-user & Roles | Staff accounts with granular permissions | `/api/v1/auth/roles/` |
| Telegram Bot | Invoice creation and stock queries via Telegram | — |
| Accounting Export | Export to standard formats (e.g., for tax submission) | `/api/v1/accounting/export/` |

---

## 7. Database Design

### Key Tables (ERD Summary)

```
customers          — id, name, phone, email, group_id, credit_limit,
                     notes, deleted_at
suppliers          — id, name, contact, phone, email, tax_id, payment_terms,
                     notes, deleted_at
bank_accounts      — id, name, type, iban, bank_name, opening_balance
categories         — id, name, parent_id, slug, image_url
tags               — id, name, color
products           — id, name, sku, barcode, category_id, type,
                     cost_price, sale_price, unit, min_stock, active, deleted_at
product_tags       — product_id, tag_id
product_attributes — id, product_id, attributes_jsonb
inventory_lots     — id, product_id, source_item_id, quantity_received,
                     quantity_remaining, unit_cost, batch_no, expiry_date
inventory_movements— id, product_id, type (IN/OUT/ADJ), quantity, reference_type,
                     reference_id, inventory_lot_id, unit_cost, note, created_at
purchase_invoices  — id, number, date, supplier_id, subtotal, discount,
                     tax, shipping, total, payment_status, notes
purchase_items     — id, invoice_id, product_id, quantity, unit_cost,
                     discount_pct, tax_pct, line_total
sale_invoices      — id, number, date, customer_id, subtotal, discount,
                     tax, total, payment_status, notes
sale_items         — id, invoice_id, product_id, quantity, unit_price,
                     discount_pct, tax_pct, line_total, unit_cost
accounts           — id, code, name, type (ASSET/LIABILITY/EQUITY/REVENUE/EXPENSE),
                     parent_id
journal_entries    — id, date, description, reference_type, reference_id,
                     created_by, created_at
journal_lines      — id, entry_id, account_id, debit, credit, note
payments           — id, reference_type (SALE/PURCHASE), reference_id,
                     amount, method, bank_account_id, date, note
```

### Design Rules

- All monetary values stored as `NUMERIC(15, 2)` — never use `FLOAT` for money
- All timestamps stored in UTC, displayed in local time on the frontend
- Soft deletes on all master data (customers, suppliers, products) — never hard delete
- Every inventory movement has a traceable `reference_type` + `reference_id`
- Journal entries are immutable after creation — corrections via reversal entries only
- Customer, supplier, bank, and inventory balances are derived from source records or controlled ledger postings; cached balance columns are allowed only if they are rebuilt and verified from the source of truth.
- FIFO valuation is implemented through `inventory_lots`, not only aggregate stock counts.
- Product custom attributes use `jsonb` with targeted indexes for searchable fields.

---

## 8. API Design Principles

- Base URL: `/api/v1/`
- Authentication: `Authorization: Bearer <JWT token>`
- All responses follow a consistent envelope:

```json
{
  "success": true,
  "data": { ... },
  "meta": { "page": 1, "total": 42 },
  "error": null
}
```

- Pagination: `?page=1&page_size=20` on all list endpoints
- Filtering: `?search=term&category_id=5&status=active`
- Sorting: `?sort_by=created_at&sort_dir=desc`
- Swagger UI auto-generated at `/docs`
- ReDoc at `/redoc`

### Key Endpoint Groups

```
POST   /api/v1/auth/login
GET    /api/v1/customers/
POST   /api/v1/customers/
GET    /api/v1/customers/{id}/statement
GET    /api/v1/suppliers/
POST   /api/v1/suppliers/
GET    /api/v1/products/
POST   /api/v1/products/
GET    /api/v1/products/{id}/inventory
GET    /api/v1/products/barcode-lookup?code=123456789
GET    /api/v1/purchase-invoices/
POST   /api/v1/purchase-invoices/
GET    /api/v1/sale-invoices/
POST   /api/v1/sale-invoices/
GET    /api/v1/sale-invoices/{id}/pdf
GET    /api/v1/accounting/journal-entries/
POST   /api/v1/accounting/journal-entries/
GET    /api/v1/accounting/trial-balance?date=2026-03-20
GET    /api/v1/reports/profit-loss?from=2026-01-01&to=2026-03-31
GET    /api/v1/reports/inventory/low-stock
GET    /api/v1/reports/sales/top-products?period=monthly
```

---

## 9. Barcode Scanner Integration

Uses **ZXing-js** (`@zxing/library`) — a pure JavaScript barcode library that works inside the browser with no native app or plugin required.

### Supported Barcode Formats

- EAN-13 (standard product barcodes)
- EAN-8
- QR Code
- Code 128
- UPC-A / UPC-E

### How It Works

1. User clicks the "Scan Barcode" button on the invoice line item form
2. A modal opens requesting camera permission
3. ZXing accesses the device camera (or webcam on laptop)
4. On successful scan, the barcode value is sent to `GET /api/v1/products/barcode-lookup?code=<value>`
5. If product found → line item is auto-filled (name, price, unit)
6. If not found → user is prompted to create the product

### Device Support

| Device | Input | Notes |
|---|---|---|
| Android phone | Rear camera | Works in Chrome, Firefox |
| iPhone | Rear/front camera | Works in Safari (iOS 14.3+) |
| Laptop | Webcam | Works in all modern browsers |
| Desktop (no camera) | Manual entry fallback | Text input always available |

---

## 10. Accounting Engine

### Automatic Journal Entry — Purchase Invoice

When a purchase invoice is saved, the system automatically creates:

```
DR  Inventory (1140)               unit_cost × qty     [per physical line item]
DR  Expense/Service Cost           service cost         [per service line item]
DR  Tax Receivable (1150)          tax amount           [if VAT applicable]
    CR  Accounts Payable (2110)    unpaid amount        [if credit or partial]
    CR  Bank Account (1120)        paid bank amount     [if paid by bank]
    CR  Cash (1110)                paid cash amount     [if paid by cash]
```

### Automatic Journal Entry — Sale Invoice

```
DR  Accounts Receivable (1130)     unpaid amount        [if credit or partial]
DR  Cash/Bank (1110/1120)          paid amount          [if paid]
DR  Cost of Goods Sold (5100)      FIFO cost × qty      [COGS]
    CR  Sales Revenue (4100)       subtotal
    CR  Tax Payable (2120)         tax amount           [if VAT applicable]
    CR  Inventory (1140)           FIFO cost × qty      [inventory reduction]
```

### Manual Journal Entries

For expenses not tied to invoices (rent, salaries, utilities):
- User selects debit account, credit account, amount, date, description
- System validates that debits = credits before saving
- Immutable after save; corrections via reversal entry

---

## 11. Reporting System

### Report Generation Flow

```
User selects report + date range
        ↓
FastAPI endpoint receives request
        ↓
Pandas DataFrame built from PostgreSQL query
        ↓
Aggregation, grouping, calculations applied
        ↓
Response: JSON (for UI charts) OR PDF (WeasyPrint) OR Excel (openpyxl)
```

### Report Caching

For expensive reports (e.g., full-year P&L), results are cached in memory for 5 minutes to avoid repeated heavy queries.

---

## 12. Implementation Guardrails

- Financial writes must be idempotent where clients may retry requests. Invoice creation should accept an idempotency key.
- Invoice, payment, inventory, and journal-entry changes must be wrapped in a single database transaction.
- Generated invoice numbers must be allocated safely under concurrent requests.
- Aggregate reports should read from canonical records and tolerate rebuilding cached summaries.
- Background jobs may be introduced later, but core invoice posting must work synchronously first.
- Offline financial writes are not supported until there is an explicit sync, locking, and conflict-resolution design.

---

## 13. Security Considerations

- JWT tokens expire after 8 hours; refresh token lasts 30 days
- All API endpoints require authentication except `/api/v1/auth/login`
- Passwords hashed with bcrypt (never stored plain)
- SQL injection prevented by SQLAlchemy parameterized queries (no raw SQL)
- CORS restricted to the frontend origin in production
- PDF invoice URLs are signed (time-limited) to prevent unauthorized access
- Database credentials stored in `.env` file (never committed to Git)
- `.env.example` provided with placeholder values for open-source users
- Refresh tokens are stored hashed, can be revoked, and rotate on use.
- Production deployments require HTTPS, secure cookies where applicable, and a documented backup/restore process.
- Administrative and financial actions are written to an audit log.
- Login and public file endpoints are rate limited.

---

## 14. Project Structure

```
TotalSell/
│
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI app entry point
│   │   ├── config.py             # Settings from .env
│   │   ├── database.py           # SQLAlchemy engine + session
│   │   ├── models/               # SQLAlchemy ORM models
│   │   │   ├── customer.py
│   │   │   ├── supplier.py
│   │   │   ├── product.py
│   │   │   ├── invoice.py
│   │   │   ├── accounting.py
│   │   │   └── inventory.py
│   │   ├── schemas/              # Pydantic request/response schemas
│   │   ├── routers/              # API route handlers (one file per module)
│   │   │   ├── customers.py
│   │   │   ├── suppliers.py
│   │   │   ├── products.py
│   │   │   ├── purchase_invoices.py
│   │   │   ├── sale_invoices.py
│   │   │   ├── accounting.py
│   │   │   ├── bank_accounts.py
│   │   │   └── reports.py
│   │   └── services/             # Business logic (cascades, calculations)
│   │       ├── invoice_service.py
│   │       ├── accounting_service.py
│   │       ├── inventory_service.py
│   │       └── report_service.py
│   ├── alembic/                  # Database migrations
│   ├── tests/                    # pytest test suite
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── routes/               # SvelteKit pages
│   │   │   ├── dashboard/
│   │   │   ├── customers/
│   │   │   ├── suppliers/
│   │   │   ├── products/
│   │   │   ├── invoices/
│   │   │   │   ├── purchase/
│   │   │   │   └── sale/
│   │   │   ├── accounting/
│   │   │   ├── inventory/
│   │   │   └── reports/
│   │   ├── lib/
│   │   │   ├── components/       # Reusable UI components
│   │   │   │   ├── BarcodeScanner.svelte
│   │   │   │   ├── InvoiceForm.svelte
│   │   │   │   ├── DataTable.svelte
│   │   │   │   └── ...
│   │   │   ├── stores/           # Svelte state stores
│   │   │   └── api/              # API client functions
│   │   └── app.html
│   ├── static/
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml            # Full stack: backend + frontend + postgres
├── .env.example                  # Environment variable template
├── README.md                     # Quick start guide
├── DESIGN.md                     # This file — architecture reference
└── CONTRIBUTING.md               # Open source contribution guide
```

---

## 15. Development Roadmap

### Phase 0 - Foundation

- [ ] Project scaffolding (FastAPI + SvelteKit + PostgreSQL + Docker)
- [ ] Authentication (JWT login)
- [ ] Base database schema and Alembic setup
- [ ] Shared API response, pagination, filtering, and error handling
- [ ] Responsive application shell

### Phase 1 - Master Data

- [ ] Customer management CRUD
- [ ] Supplier management CRUD
- [ ] Category & tag management
- [ ] Product & service management CRUD
- [ ] Product custom attributes and searchable indexes

### Phase 2 - Transaction Core

- [ ] Bank account management
- [ ] Purchase invoice (with auto accounting + inventory cascade)
- [ ] Sale invoice (with auto accounting + inventory cascade)
- [ ] Inventory tracking & movement history
- [ ] Payment tracking with partial payment support
- [ ] FIFO inventory lots and stock valuation

### Phase 3 - Accounting Core

- [ ] Chart of accounts + manual journal entries
- [ ] General ledger view
- [ ] Basic reports (P&L, balance sheet, trial balance)

### Phase 4 - Reporting and Exports

- [ ] Sales & purchase reports
- [ ] Inventory reports (low stock alerts)
- [ ] PDF invoice generation
- [ ] Excel report export

### Phase 5 - Mobile and Workflow Polish

- [ ] Barcode scanner integration
- [ ] Responsive UI (mobile-first)
- [ ] PWA installability and offline static asset support

### Phase 6 - Operations Enhancement

- [ ] Multi-user support with role-based access (Admin, Staff, Accountant)
- [ ] Customer loyalty points system
- [ ] Supplier price lists and purchase order management
- [ ] Advanced inventory: FIFO valuation, batch/lot tracking with expiry dates
- [ ] Automated low-stock email / push notifications
- [ ] Dashboard analytics with charts (Chart.js)
- [ ] Data import (products, customers via Excel)
- [ ] Telegram bot for quick stock queries and invoice creation

### Phase 7 - Customer-Facing

- [ ] Online storefront (product catalog, cart, order placement)
- [ ] Payment gateway integration
- [ ] Customer portal (order history, invoice download)
- [ ] CRM: tickets, follow-ups, notes
- [ ] Logistics: shipping methods, tracking
- [ ] SMS / email notifications to customers

### Phase 8 - Open Source Maturity

- [ ] Full test suite (pytest backend, Playwright frontend)
- [ ] Docker Hub image publishing
- [ ] One-click deployment guide (VPS / Hetzner / Linode)
- [ ] Persian language documentation
- [ ] English documentation
- [ ] Demo instance (live preview)

---

## 16. Open Source Guidelines

### License

MIT License — free to use, modify, and distribute with attribution.

### Contributing

See `CONTRIBUTING.md` for:
- How to set up the development environment
- Coding style guidelines (Black for Python, Prettier for JS)
- How to submit a pull request
- How to report bugs and request features

### Environment Setup for Contributors

```bash
# Clone the repo
git clone https://github.com/your-username/TotalSell.git
cd TotalSell

# Copy environment template
cp .env.example .env
# Edit .env with your local settings

# Start everything with Docker
docker-compose up --build

# Backend API available at:  http://localhost:8000
# Swagger docs at:           http://localhost:8000/docs
# Frontend at:               http://localhost:5173
```

### Design Decisions Log

| Decision | Rationale |
|---|---|
| SvelteKit over React | Lower learning curve, less boilerplate, better mobile perf |
| FastAPI over Django | Lighter weight, async, auto docs, ideal for API-only backend |
| PostgreSQL over SQLite | ACID compliance required for financial data |
| Double-entry accounting | Industry standard, audit-ready, extensible to full accounting |
| FIFO inventory | Standard for retail, accurate cost tracking |
| ZXing-js for barcode | No native app needed, works on all devices in browser |
| WeasyPrint for PDF | HTML/CSS templates, easy to customize invoice design |
| Soft deletes | Financial records must never be hard-deleted |
| JWT over sessions | Stateless, works for future mobile app and Telegram bot |
| Flexible custom attributes | Allows any business type to add domain-specific fields per category |

---

*This document is a living reference. Update it whenever architectural decisions change.*
