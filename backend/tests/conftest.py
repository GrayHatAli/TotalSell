import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

os.environ["ENVIRONMENT"] = "test"
os.environ["DATABASE_URL"] = "sqlite:///./test_totalsell.db"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-local-test-suite"
os.environ["ADMIN_EMAIL"] = "admin@example.com"
os.environ["ADMIN_PASSWORD"] = "ChangeMe123!"

from app.database import engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Base  # noqa: E402
from app.seed import seed_accounts, seed_admin  # noqa: E402
from app.database import SessionLocal  # noqa: E402


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_admin(db)
        seed_accounts(db)
    finally:
        db.close()
    yield


@pytest.fixture
def client():
    return TestClient(app)


def pytest_sessionfinish(session, exitstatus):
    db_path = Path("test_totalsell.db")
    if db_path.exists():
        db_path.unlink()

