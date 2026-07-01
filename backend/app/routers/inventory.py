from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.inventory import InventoryMovement
from app.schemas.common import ok
from app.services.auth import get_current_user

router = APIRouter(prefix="/inventory-movements", tags=["inventory-movements"])


@router.get("")
def list_inventory_movements(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
    product_id: int | None = None,
    movement_type: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    query = db.query(InventoryMovement)
    if product_id is not None:
        query = query.filter(InventoryMovement.product_id == product_id)
    if movement_type is not None:
        query = query.filter(InventoryMovement.movement_type == movement_type)
    query = query.order_by(desc(InventoryMovement.created_at))
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    results = []
    for m in items:
        results.append({
            "id": m.id,
            "product_id": m.product_id,
            "movement_type": m.movement_type,
            "quantity": float(m.quantity),
            "unit_cost": float(m.unit_cost),
            "reference_type": m.reference_type,
            "reference_id": m.reference_id,
            "note": m.note,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        })
    return ok(results, meta={"page": page, "page_size": page_size, "total": total})
