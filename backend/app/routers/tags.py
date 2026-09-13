from datetime import UTC, datetime

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.tag import Tag
from app.schemas.common import ok
from app.schemas.tag import TagCreate, TagResponse, TagUpdate
from app.services.auth import get_current_user
from app.services.excel import read_spreadsheet_rows

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


@router.post("/import")
def import_tags(file: UploadFile = File(...), db: Session = Depends(get_db), _user=Depends(get_current_user)):
    """Import tags from an Excel file.

    Expected columns (first row = header):
      name (required, English or "نام"/"برچسب"), color (optional, "رنگ")
    - Rows with an existing name are skipped as duplicates.
    - color accepts hex (#ff0000) or plain text up to 20 chars; blank = no color.
    """
    rows = read_spreadsheet_rows(file)

    header = [str(c or "").strip().lower() if c is not None else "" for c in rows[0]]

    def col_idx(*names: str) -> int | None:
        for i, h in enumerate(header):
            if h in names:
                return i
        return None

    name_idx = col_idx("name", "tag", "نام", "برچسب")
    if name_idx is None:
        raise HTTPException(status_code=400, detail='Missing required column "name"')
    color_idx = col_idx("color", "رنگ")

    created, skipped, failed = 0, 0, 0
    errors: list[dict] = []
    for row_num, row in enumerate(rows[1:], start=2):
        name = str(row[name_idx]).strip() if row[name_idx] is not None else ""
        if not name:
            failed += 1
            errors.append({"row": row_num, "reason": "name is required"})
            continue
        if len(name) > 100:
            failed += 1
            errors.append({"row": row_num, "reason": "name is longer than 100 characters"})
            continue
        # Tag.name has a DB-level UNIQUE constraint, so duplicates (from this
        # file or the DB) are skipped.
        if db.query(Tag).filter(Tag.name == name).first():
            skipped += 1
            continue
        color = None
        if color_idx is not None and row[color_idx] is not None:
            color = str(row[color_idx]).strip()[:20] or None
        db.add(Tag(name=name, color=color))
        # Flush so tags created earlier in this file are visible to the
        # duplicate check of subsequent rows (session has autoflush disabled).
        db.flush()
        created += 1
    db.commit()
    return ok(
        {"created": created, "skipped": skipped, "failed": failed, "errors": errors},
        meta={"total_rows": len(rows) - 1},
    )


@router.get("/{tag_id}")
def get_tag(tag_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    tag = db.get(Tag, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return ok(TagResponse.model_validate(tag))


@router.patch("/{tag_id}")
def update_tag(tag_id: int, payload: TagUpdate, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    tag = db.get(Tag, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    if payload.name:
        exists = db.query(Tag).filter(Tag.name == payload.name, Tag.id != tag_id).first()
        if exists:
            raise HTTPException(status_code=400, detail="Tag name already exists")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(tag, key, value)
    db.commit()
    db.refresh(tag)
    return ok(TagResponse.model_validate(tag))


@router.delete("/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db), _user=Depends(get_current_user)):
    tag = db.get(Tag, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(tag)
    db.commit()
    return ok({"status": "deleted"})
