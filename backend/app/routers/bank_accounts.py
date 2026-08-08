from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.bank_account import BankAccount
from app.schemas.bank_account import BankAccountCreate, BankAccountResponse, BankAccountUpdate
from app.schemas.common import ok
from app.services.auth import get_current_user

router = APIRouter(prefix="/bank-accounts", tags=["bank-accounts"])


@router.get("")
def list_bank_accounts(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
    search: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    query = db.query(BankAccount).filter(BankAccount.deleted_at.is_(None))
    if search:
        like = f"%{search}%"
        query = query.filter(or_(BankAccount.name.ilike(like), BankAccount.bank_name.ilike(like)))
    items = query.order_by(BankAccount.name).offset((page - 1) * page_size).limit(page_size).all()
    total = query.count()
    return ok([BankAccountResponse.model_validate(i).model_dump(mode="json") for i in items], meta={"page": page, "page_size": page_size, "total": total})


@router.post("")
def create_bank_account(payload: BankAccountCreate, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    account = BankAccount(**payload.model_dump())
    db.add(account)
    db.commit()
    db.refresh(account)
    return ok(BankAccountResponse.model_validate(account).model_dump(mode="json"), meta={"id": account.id})


@router.get("/{account_id}")
def get_bank_account(account_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    account = db.get(BankAccount, account_id)
    if account is None or account.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Bank account not found")
    return ok(BankAccountResponse.model_validate(account).model_dump(mode="json"))


@router.patch("/{account_id}")
def update_bank_account(account_id: int, payload: BankAccountUpdate, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    account = db.get(BankAccount, account_id)
    if account is None or account.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Bank account not found")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(account, key, value)
    db.commit()
    db.refresh(account)
    return ok(BankAccountResponse.model_validate(account).model_dump(mode="json"))


@router.delete("/{account_id}")
def delete_bank_account(account_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    account = db.get(BankAccount, account_id)
    if account is None or account.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Bank account not found")
    from datetime import UTC, datetime
    account.deleted_at = datetime.now(UTC)
    db.add(account)
    db.commit()
    return ok({"status": "deleted"})
