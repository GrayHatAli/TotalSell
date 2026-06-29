from datetime import UTC, datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models.user import RefreshToken, User
from app.schemas.auth import TokenResponse
from app.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    hash_token,
    verify_password,
)


bearer_scheme = HTTPBearer(auto_error=False)


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email).one_or_none()
    if user is None or not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def issue_token_pair(db: Session, user: User) -> TokenResponse:
    settings = get_settings()
    access_token, expires_at = create_access_token(str(user.id))
    refresh_token = create_refresh_token()
    refresh_record = RefreshToken(
        user_id=user.id,
        token_hash=hash_token(refresh_token),
        expires_at=datetime.now(UTC) + timedelta(days=settings.refresh_token_days),
    )
    db.add(refresh_record)
    db.commit()
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, expires_at=expires_at)


def refresh_token_pair(db: Session, refresh_token: str) -> TokenResponse | None:
    token_hash = hash_token(refresh_token)
    token_record = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).one_or_none()
    now = datetime.now(UTC)
    if token_record is None or token_record.revoked_at is not None or token_record.expires_at < now:
        return None

    user = db.get(User, token_record.user_id)
    if user is None or not user.is_active:
        return None

    token_record.revoked_at = now
    db.add(token_record)
    db.flush()
    return issue_token_pair(db, user)


def revoke_refresh_token(db: Session, refresh_token: str) -> None:
    token_record = db.query(RefreshToken).filter(RefreshToken.token_hash == hash_token(refresh_token)).one_or_none()
    if token_record is not None and token_record.revoked_at is None:
        token_record.revoked_at = datetime.now(UTC)
        db.add(token_record)
        db.commit()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    try:
        subject = decode_access_token(credentials.credentials)
        user_id = int(subject)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid bearer token") from exc

    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive or missing user")
    return user

