import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models.user import User, UserRole
from app.models.record import Record, RecordType, Category
from app.middleware.auth import hash_password, create_access_token
from datetime import date
TEST_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "test.db")
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
    if os.path.exists(TEST_DB_PATH):
        try:
            os.remove(TEST_DB_PATH)
        except OSError:
            pass
@pytest.fixture
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
@pytest.fixture
def client(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
@pytest.fixture
def admin_user(db_session):
    user = User(
        username="testadmin",
        email="admin@test.com",
        password_hash=hash_password("admin123"),
        role=UserRole.ADMIN,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
@pytest.fixture
def analyst_user(db_session):
    user = User(
        username="testanalyst",
        email="analyst@test.com",
        password_hash=hash_password("analyst123"),
        role=UserRole.ANALYST,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
@pytest.fixture
def viewer_user(db_session):
    user = User(
        username="testviewer",
        email="viewer@test.com",
        password_hash=hash_password("viewer123"),
        role=UserRole.VIEWER,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
@pytest.fixture
def admin_token(admin_user):
    return create_access_token(data={"sub": str(admin_user.id), "role": "admin"})
@pytest.fixture
def analyst_token(analyst_user):
    return create_access_token(data={"sub": str(analyst_user.id), "role": "analyst"})
@pytest.fixture
def viewer_token(viewer_user):
    return create_access_token(data={"sub": str(viewer_user.id), "role": "viewer"})
@pytest.fixture
def sample_records(db_session, admin_user):
    records = [
        Record(user_id=admin_user.id, amount=5000, type=RecordType.INCOME, category=Category.SALARY, date=date(2025, 1, 1), description="January salary"),
        Record(user_id=admin_user.id, amount=1200, type=RecordType.INCOME, category=Category.FREELANCE, date=date(2025, 1, 15), description="Freelance work"),
        Record(user_id=admin_user.id, amount=800, type=RecordType.EXPENSE, category=Category.FOOD, date=date(2025, 1, 10), description="Groceries"),
        Record(user_id=admin_user.id, amount=1200, type=RecordType.EXPENSE, category=Category.UTILITIES, date=date(2025, 1, 5), description="Rent"),
        Record(user_id=admin_user.id, amount=5000, type=RecordType.INCOME, category=Category.SALARY, date=date(2025, 2, 1), description="February salary"),
        Record(user_id=admin_user.id, amount=400, type=RecordType.EXPENSE, category=Category.ENTERTAINMENT, date=date(2025, 2, 14), description="Entertainment"),
    ]
    db_session.add_all(records)
    db_session.commit()
    for r in records:
        db_session.refresh(r)
    return records