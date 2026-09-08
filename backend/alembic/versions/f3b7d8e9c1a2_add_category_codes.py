"""add category codes (hierarchical accounting-style numbering)

Revision ID: f3b7d8e9c1a2
Revises: d9f1c2a4e8b0
Create Date: 2026-01-15

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "f3b7d8e9c1a2"
down_revision: str | None = "d9f1c2a4e8b0"
branch_labels = None
depends_on = None


def _allocate(used: set[str], parent_code: str | None, child_level: int) -> str:
    """Next free code for a category at `child_level` under `parent_code`."""
    if parent_code is None:
        n = 1
        while str(1000 * n) in used:
            n += 1
        return str(1000 * n)
    pc = int(parent_code)
    if child_level <= 4:
        step = 10 ** (4 - child_level)
        n = 1
        while str(pc + step * n) in used:
            n += 1
        return str(pc + step * n)
    n = 1
    while str(pc * 10 + n) in used:
        n += 1
    return str(pc * 10 + n)


def upgrade() -> None:
    op.add_column("categories", sa.Column("code", sa.String(20), nullable=True))
    # Unique index instead of a constraint: works on SQLite too, and allows
    # multiple NULLs for legacy/manual rows.
    op.create_index("uq_categories_code", "categories", ["code"], unique=True)

    conn = op.get_bind()
    rows = conn.execute(sa.text("SELECT id, parent_id FROM categories ORDER BY id")).fetchall()
    parent_of = {r.id: r.parent_id for r in rows}
    children: dict = {}
    for r in rows:
        children.setdefault(r.parent_id, []).append(r.id)

    def level_of(cid: int) -> int:
        lvl, cur, seen = 1, cid, set()
        while parent_of.get(cur) is not None and cur not in seen:
            seen.add(cur)
            cur = parent_of[cur]
            lvl += 1
        return lvl

    codes: dict = {}
    used: set[str] = set()
    queue = list(children.get(None, []))
    while queue:
        next_queue = []
        for cid in queue:
            parent_id = parent_of.get(cid)
            parent_code = codes.get(parent_id) if parent_id is not None else None
            code = _allocate(used, parent_code, level_of(cid))
            codes[cid] = code
            used.add(code)
            next_queue.extend(children.get(cid, []))
        queue = next_queue

    for cid, code in codes.items():
        conn.execute(sa.text("UPDATE categories SET code = :c WHERE id = :i"), {"c": code, "i": cid})


def downgrade() -> None:
    op.drop_index("uq_categories_code", table_name="categories")
    op.drop_column("categories", "code")