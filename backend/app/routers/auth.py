from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, LogoutRequest, RefreshRequest, UserResponse
from app.schemas.common import ok
from app.services.auth import (
    authenticate_user,
    get_current_user,
    issue_token_pair,
    refresh_token_pair,
    revoke_refresh_token,
)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> dict:
    user = authenticate_user(db, payload.email, payload.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return ok(issue_token_pair(db, user).model_dump(mode="json"))


@router.post("/refresh")
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)) -> dict:
    token_pair = refresh_token_pair(db, payload.refresh_token)
    if token_pair is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    return ok(token_pair.model_dump(mode="json"))


@router.post("/logout")
def logout(payload: LogoutRequest, db: Session = Depends(get_db)) -> dict:
    if payload.refresh_token:
        revoke_refresh_token(db, payload.refresh_token)
    return ok({"status": "logged_out"})


@router.get("/me")
def me(current_user: User = Depends(get_current_user)) -> dict:
    user = UserResponse(
        id=current_user.id,
        email=current_user.email,
        is_active=current_user.is_active,
        is_admin=current_user.is_admin,
    )
    return ok(user.model_dump(mode="json"))

