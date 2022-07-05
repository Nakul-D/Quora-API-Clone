from app.main import app
from app.config import settings
from app.utils import password_functions
from app.database.database import get_db
from app.database.models import Base, User, Question
from app.utils.token_functions import create_access_token
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
def test_user_1(session) -> dict:
    user = User(
        email = "testemail@gmail.com",
        password = password_functions.hash_password("123456789"),
        username = "test_user",
        bio = "test"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"email": user.email, "password": "123456789", "username": user.username, "bio": user.bio, "userId": user.userId}

@pytest.fixture
def test_user_2(session) -> dict:
    user = User(
        email = "testemail2@gmail.com",
        password = password_functions.hash_password("123456789"),
        username = "test_user_2",
        bio = "test_2"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"email": user.email, "password": "123456789", "username": user.username, "bio": user.bio, "userId": user.userId}

@pytest.fixture
def authorized_client_1(client, test_user_1):
    token = create_access_token({'id': test_user_1['userId']})
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}'
    }
    return client

@pytest.fixture
def authorized_client_2(client, test_user_2):
    token = create_access_token({'id': test_user_2['userId']})
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}'
    }
    return client

@pytest.fixture
def create_test_questions(session, test_user_1):
    data = [
        {'question': 'test question 1', 'userId': test_user_1['userId']},
        {'question': 'test question 2', 'userId': test_user_1['userId']}
    ]
    def create_question_model(question: dict):
        return Question(**question)
    questions = list(map(create_question_model, data))
    session.add_all(questions)
    session.commit()
    return questions
