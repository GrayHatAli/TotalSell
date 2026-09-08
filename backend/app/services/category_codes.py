"""Hierarchical category codes (accounting-style numbering).

Scheme:
- Root categories are numbered in steps of 1000: 1000, 2000, ...
- Level-2 children in steps of 100: 1100, 1200, ...
- Level-3 in steps of 10: 1210, 1220, ...
- Level-4 in steps of 1: 1211, 1212, ...
- Level 5+ falls back to parent_code * 10 + n.

Products created without an explicit SKU get one derived from their
category code: "{category_code}-{serial:04d}" (e.g. 1210-0001). The
serial space is separate from the category numbering, so products never
collide with future subcategory codes and each category can hold
unlimited products.
"""


from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.product import Product

MAX_DIGITS = 4


def _category_level(db: Session, category: Category) -> int:
    """1-based depth of a category (root == 1)."""
    level = 1
    seen: set[int] = set()
    current = category
    while current.parent_id is not None and current.id not in seen:
        seen.add(current.id)
        parent = db.get(Category, current.parent_id)
        if parent is None:
            break
        level += 1
        current = parent
    return level


def next_category_code(db: Session, parent: Category | None) -> str:
    """Allocate the next free hierarchical code for a child of `parent`
    (or a new root when `parent` is None)."""
    used = {code for (code,) in db.query(Category.code).filter(Category.code.isnot(None)).all() if code}
    if parent is None or not parent.code or not parent.code.isdigit():
        n = 1
        while str(1000 * n) in used:
            n += 1
        return str(1000 * n)
    level = _category_level(db, parent) + 1
    pc = int(parent.code)
    if level <= MAX_DIGITS:
        step = 10 ** (MAX_DIGITS - level)
        n = 1
        while str(pc + step * n) in used:
            n += 1
        return str(pc + step * n)
    n = 1
    while str(pc * 10 + n) in used:
        n += 1
    return str(pc * 10 + n)


def next_product_sku(db: Session, category: Category) -> str | None:
    """Next auto SKU for a product in `category`, e.g. "1210-0001".

    Scans ALL products (including soft-deleted) because the SKU column has
    a DB-level UNIQUE constraint. Non-numeric tails (manual SKUs that
    merely share the prefix) are ignored.
    """
    if not category.code:
        return None
    prefix = f"{category.code}-"
    rows = db.query(Product.sku).filter(Product.sku.like(f"{prefix}%")).all()
    max_serial = 0
    for (sku,) in rows:
        tail = sku[len(prefix):]
        if tail.isdigit():
            max_serial = max(max_serial, int(tail))
    return f"{prefix}{max_serial + 1:04d}"