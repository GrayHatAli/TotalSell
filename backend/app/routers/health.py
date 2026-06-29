from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.common import ok


router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health() -> dict:
    return ok({"status": "ok"})


@router.get("/db")
def database_health(db: Session = Depends(get_db)) -> dict:
    db.execute(text("SELECT 1"))
    return ok({"status": "ok"})

