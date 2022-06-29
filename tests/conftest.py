from app.main import app
from app.config import settings
from app.database.models import Base, User
from app.database.database import get_db
from app.utils import password_functions
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}-test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def test_user(session) -> dict:
    user = User(
        email = "testemail@gmail.com",
        password = password_functions.hash_password("123456789"),
        username = "test_user",
        bio = "test"
    )
    session.add(user)
    session.commit()
    return {"email": user.email, "password": "123456789", "username": user.username, "bio": user.bio}
