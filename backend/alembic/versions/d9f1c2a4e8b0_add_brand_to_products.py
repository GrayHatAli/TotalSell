"""add brand to products

Revision ID: d9f1c2a4e8b0
Revises: c5e1a8f4d2b3
Create Date: 2026-09-06 12:30:00.000000
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "d9f1c2a4e8b0"
down_revision: str | None = "c5e1a8f4d2b3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("products", sa.Column("brand", sa.String(length=120), nullable=True))


def downgrade() -> None:
    op.drop_column("products", "brand")