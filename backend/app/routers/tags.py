from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.tag import Tag
from app.schemas.common import ok
from app.schemas.tag import TagCreate, TagResponse
from app.services.auth import get_current_user

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("")
def list_tags(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
    search: str | None = Query(default=None),
):
    query = db.query(Tag)
    if search:
        like = f"%{search}%"
        query = query.filter(Tag.name.ilike(like))
    items = query.order_by(Tag.name).all()
    return ok([TagResponse.model_validate(i).model_dump(mode="json") for i in items])


@router.post("")
def create_tag(payload: TagCreate, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    existing = db.query(Tag).filter(Tag.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tag already exists")
    tag = Tag(**payload.model_dump())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return ok(TagResponse.model_validate(tag).model_dump(mode="json"), meta={"id": tag.id})
