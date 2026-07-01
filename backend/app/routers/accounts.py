from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.account import Account
from app.schemas.account import AccountResponse
from app.schemas.common import ok
from app.services.auth import get_current_user

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("")
def list_accounts(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    accounts = db.query(Account).filter(Account.is_active.is_(True)).order_by(Account.code).all()
    return ok([AccountResponse.model_validate(a).model_dump(mode="json") for a in accounts])
