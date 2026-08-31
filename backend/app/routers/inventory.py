from datetime import UTC, datetime

from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.inventory import InventoryLot, InventoryMovement, LotAllocation
from app.models.product import Product
from app.models.user import AuditLog
from app.schemas.common import ok
from app.services.auth import get_current_user


class InventoryAdjustmentCreate(BaseModel):
    product_id: int = Field(..., ge=1)
    quantity: float = Field(..., gt=0)
    unit_cost: float = Field(ge=0)
    reason: str = Field(..., min_length=3, max_length=500)


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


@router.post("/adjustments", status_code=200)
def create_inventory_adjustment(
    payload: InventoryAdjustmentCreate,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    """Record a controlled stock adjustment (shrinkage/count correction).

    Arbitrary movement creation is intentionally not supported: inbound stock
    comes from purchase invoices, outbound from sale invoices, and adjustments
    require an authenticated actor plus an auditable reason.
    """
    product = db.get(Product, payload.product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.deleted_at is not None or not product.active:
        raise HTTPException(status_code=422, detail="Product is not active")

    available = (
        db.query(func.coalesce(func.sum(InventoryLot.remaining_quantity), 0))
        .filter(InventoryLot.product_id == product.id)
        .scalar()
    )
    available = Decimal(str(available))
    adjustment = Decimal(str(payload.quantity))
    if adjustment > available:
        raise HTTPException(
            status_code=422,
            detail=f"Adjustment exceeds available stock: requested {adjustment}, available {available}",
        )

    # Consume the adjustment FIFO from cost layers so lots stay authoritative.
    remaining = adjustment
    for lot in (
        db.query(InventoryLot)
        .filter(InventoryLot.product_id == product.id, InventoryLot.remaining_quantity > 0)
        .order_by(InventoryLot.id)
        .all()
    ):
        if remaining <= 0:
            break
        lot_qty = Decimal(str(lot.remaining_quantity))
        take = min(lot_qty, remaining)
        lot.remaining_quantity = lot_qty - take
        db.add(
            LotAllocation(
                lot_id=lot.id,
                product_id=product.id,
                quantity=take,
                unit_cost=lot.unit_cost,
                reference_type="ADJUSTMENT",
                reference_id=None,
            )
        )
        remaining -= take

    movement = InventoryMovement(
        product_id=payload.product_id,
        movement_type="ADJ",
        quantity=adjustment,
        unit_cost=Decimal(str(payload.unit_cost)),
        reference_type="ADJUSTMENT",
        reference_id=None,
        note=payload.reason,
    )
    db.add(movement)
    db.flush()
    db.add(
        AuditLog(
            actor_user_id=getattr(_user, "id", None),
            action="inventory_adjustment",
            details=(
                f"product_id={payload.product_id} quantity={payload.quantity} "
                f"reason={payload.reason} movement_id={movement.id}"
            ),
            created_at=datetime.now(UTC),
        )
    )
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
