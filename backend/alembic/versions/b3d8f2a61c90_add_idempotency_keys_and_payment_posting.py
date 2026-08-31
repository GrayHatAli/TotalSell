"""add idempotency keys and payment journal link

Revision ID: b3d8f2a61c90
Revises: 20e7b2359937
Create Date: 2026-08-31 12:00:00.000000

Phase 1 transaction integrity: idempotency keys for invoices and payments,
and a traceability link from payments to their posted journal entry.

Uses batch_alter_table so the migration also runs on SQLite in development
and the test suite (batch mode is a pass-through for PostgreSQL ALTERs).
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = 'b3d8f2a61c90'
down_revision: str | None = '20e7b2359937'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table('sale_invoices') as batch:
        batch.add_column(sa.Column('idempotency_key', sa.String(length=100), nullable=True))
        batch.create_index(op.f('ix_sale_invoices_idempotency_key'), ['idempotency_key'], unique=True)

    with op.batch_alter_table('purchase_invoices') as batch:
        batch.add_column(sa.Column('idempotency_key', sa.String(length=100), nullable=True))
        batch.create_index(op.f('ix_purchase_invoices_idempotency_key'), ['idempotency_key'], unique=True)

    with op.batch_alter_table('payments') as batch:
        batch.add_column(sa.Column('idempotency_key', sa.String(length=100), nullable=True))
        batch.create_index(op.f('ix_payments_idempotency_key'), ['idempotency_key'], unique=True)
        batch.add_column(sa.Column('journal_entry_id', sa.Integer(), nullable=True))
        batch.create_foreign_key(
            'fk_payments_journal_entry_id_payments',
            'journal_entries',
            ['journal_entry_id'],
            ['id'],
        )


def downgrade() -> None:
    with op.batch_alter_table('payments') as batch:
        batch.drop_constraint('fk_payments_journal_entry_id_payments', type_='foreignkey')
        batch.drop_column('journal_entry_id')
        batch.drop_index(op.f('ix_payments_idempotency_key'))
        batch.drop_column('idempotency_key')

    with op.batch_alter_table('purchase_invoices') as batch:
        batch.drop_index(op.f('ix_purchase_invoices_idempotency_key'))
        batch.drop_column('idempotency_key')

    with op.batch_alter_table('sale_invoices') as batch:
        batch.drop_index(op.f('ix_sale_invoices_idempotency_key'))
        batch.drop_column('idempotency_key')
