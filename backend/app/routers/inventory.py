from datetime import UTC, datetime

from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.inventory import InventoryMovement
from app.models.product import Product
from app.schemas.common import ok
from app.services.auth import get_current_user


class InventoryMovementCreate(BaseModel):
    product_id: int = Field(..., ge=1)
    movement_type: str = Field(..., pattern="^(IN|OUT|ADJ)$")
    quantity: float = Field(..., gt=0)
    unit_cost: float = Field(ge=0)
    reference_type: str | None = None
    reference_id: int | None = None
    note: str | None = None


router = APIRouter(prefix="/inventory-movements", tags=["inventory"])


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


@router.post("")
def create_inventory_movement(payload: InventoryMovementCreate, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    # Check if product exists
    product = db.get(Product, payload.product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    movement = InventoryMovement(
        product_id=payload.product_id,
        movement_type=payload.movement_type,
        quantity=payload.quantity,
        unit_cost=payload.unit_cost,
        reference_type=payload.reference_type,
        reference_id=payload.reference_id,
        note=payload.note,
    )
    db.add(movement)
    db.commit()
    db.refresh(movement)
    return ok({
        "id": movement.id,
        "product_id": movement.product_id,
        "movement_type": movement.movement_type,
        "quantity": float(movement.quantity),
        "unit_cost": float(movement.unit_cost),
        "reference_type": movement.reference_type,
        "reference_id": movement.reference_id,
        "note": movement.note,
        "created_at": movement.created_at.isoformat() if movement.created_at else None,
    }, meta={"id": movement.id})
