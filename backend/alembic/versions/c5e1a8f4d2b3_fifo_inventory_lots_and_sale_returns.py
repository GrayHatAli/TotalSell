"""fifo inventory lots, allocations, and sale returns

Revision ID: c5e1a8f4d2b3
Revises: b3d8f2a61c90
Create Date: 2026-08-31 14:00:00.000000

Phase 2 inventory correctness: FIFO cost layers (inventory_lots) consumed by
persisted allocations (lot_allocations), plus the sale return (credit note)
workflow. Existing movement history is backfilled into one aggregate lot per
product so stock and valuation remain correct for legacy data.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = 'c5e1a8f4d2b3'
down_revision: str | None = 'b3d8f2a61c90'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'inventory_lots',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('source_type', sa.String(length=50), nullable=False, server_default='PURCHASE_INVOICE'),
        sa.Column('source_id', sa.Integer(), nullable=True),
        sa.Column('received_quantity', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('remaining_quantity', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('unit_cost', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('batch_number', sa.String(length=100), nullable=True),
        sa.Column('expiry_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_inventory_lots_id'), 'inventory_lots', ['id'], unique=False)
    op.create_index(op.f('ix_inventory_lots_product_id'), 'inventory_lots', ['product_id'], unique=False)

    op.create_table(
        'lot_allocations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lot_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('unit_cost', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('reference_type', sa.String(length=50), nullable=False),
        sa.Column('reference_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['lot_id'], ['inventory_lots.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_lot_allocations_id'), 'lot_allocations', ['id'], unique=False)
    op.create_index(op.f('ix_lot_allocations_lot_id'), 'lot_allocations', ['lot_id'], unique=False)
    op.create_index(op.f('ix_lot_allocations_product_id'), 'lot_allocations', ['product_id'], unique=False)
    op.create_index(op.f('ix_lot_allocations_reference_type'), 'lot_allocations', ['reference_type'], unique=False)

    op.create_table(
        'sale_returns',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('number', sa.String(length=50), nullable=False),
        sa.Column('sale_invoice_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('subtotal', sa.Numeric(precision=15, scale=2), nullable=False, server_default='0'),
        sa.Column('tax_amount', sa.Numeric(precision=15, scale=2), nullable=False, server_default='0'),
        sa.Column('cogs_amount', sa.Numeric(precision=15, scale=2), nullable=False, server_default='0'),
        sa.Column('total', sa.Numeric(precision=15, scale=2), nullable=False, server_default='0'),
        sa.Column('journal_entry_id', sa.Integer(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['sale_invoice_id'], ['sale_invoices.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['journal_entry_id'], ['journal_entries.id']),
        sa.ForeignKeyConstraint(['created_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_sale_returns_id'), 'sale_returns', ['id'], unique=False)
    op.create_index(op.f('ix_sale_returns_number'), 'sale_returns', ['number'], unique=True)
    op.create_index(op.f('ix_sale_returns_sale_invoice_id'), 'sale_returns', ['sale_invoice_id'], unique=False)
    op.create_index(op.f('ix_sale_returns_date'), 'sale_returns', ['date'], unique=False)

    op.create_table(
        'sale_return_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('return_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=True),
        sa.Column('quantity', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('unit_price', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('tax_pct', sa.Numeric(precision=5, scale=2), nullable=False, server_default='0'),
        sa.Column('line_total', sa.Numeric(precision=15, scale=2), nullable=False, server_default='0'),
        sa.Column('unit_cost', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.ForeignKeyConstraint(['return_id'], ['sale_returns.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_sale_return_items_id'), 'sale_return_items', ['id'], unique=False)
    op.create_index(op.f('ix_sale_return_items_return_id'), 'sale_return_items', ['return_id'], unique=False)
    op.create_index(op.f('ix_sale_return_items_product_id'), 'sale_return_items', ['product_id'], unique=False)

    # Backfill one aggregate opening lot per product from legacy movements so
    # remaining stock and valuation survive the switch to lot-based accounting.
    op.execute(
        """
        INSERT INTO inventory_lots
            (product_id, source_type, source_id, received_quantity, remaining_quantity,
             unit_cost, batch_number, expiry_date, created_at, updated_at)
        SELECT
            m.product_id,
            'MIGRATION_BACKFILL',
            NULL,
            SUM(CASE WHEN m.movement_type = 'IN' THEN m.quantity ELSE 0 END),
            CASE
                WHEN SUM(CASE WHEN m.movement_type = 'IN' THEN m.quantity ELSE -m.quantity END) < 0 THEN 0
                ELSE SUM(CASE WHEN m.movement_type = 'IN' THEN m.quantity ELSE -m.quantity END)
            END,
            COALESCE(
                SUM(CASE WHEN m.movement_type = 'IN' THEN m.quantity * m.unit_cost ELSE 0 END)
                / NULLIF(SUM(CASE WHEN m.movement_type = 'IN' THEN m.quantity ELSE 0 END), 0),
                0
            ),
            NULL, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
        FROM inventory_movements m
        GROUP BY m.product_id
        HAVING SUM(CASE WHEN m.movement_type = 'IN' THEN m.quantity ELSE 0 END) > 0
        """
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_sale_return_items_id'), table_name='sale_return_items')
    op.drop_index(op.f('ix_sale_return_items_product_id'), table_name='sale_return_items')
    op.drop_index(op.f('ix_sale_return_items_return_id'), table_name='sale_return_items')
    op.drop_table('sale_return_items')
    op.drop_index(op.f('ix_sale_returns_id'), table_name='sale_returns')
    op.drop_index(op.f('ix_sale_returns_date'), table_name='sale_returns')
    op.drop_index(op.f('ix_sale_returns_sale_invoice_id'), table_name='sale_returns')
    op.drop_index(op.f('ix_sale_returns_number'), table_name='sale_returns')
    op.drop_table('sale_returns')
    op.drop_index(op.f('ix_lot_allocations_id'), table_name='lot_allocations')
    op.drop_index(op.f('ix_lot_allocations_reference_type'), table_name='lot_allocations')
    op.drop_index(op.f('ix_lot_allocations_product_id'), table_name='lot_allocations')
    op.drop_index(op.f('ix_lot_allocations_lot_id'), table_name='lot_allocations')
    op.drop_table('lot_allocations')
    op.drop_index(op.f('ix_inventory_lots_id'), table_name='inventory_lots')
    op.drop_index(op.f('ix_inventory_lots_product_id'), table_name='inventory_lots')
    op.drop_table('inventory_lots')

