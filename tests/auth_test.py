from app.config import settings
from app.database import models
from app.routers.auth import schemas
import pytest
from jose import jwt


@pytest.mark.parametrize(
    "email, username, password, bio", [
        ("testemail@gmail.com", "test_user", "123456789", None),
        ("testemail@gmail.com", "test_user", None, "testing"),
        ("testemail@gmail.com", None, "123456789", "testing"),
        (None, "test_user", "123456789", "testing"),
        ("testemail", "test_user", "123456789", "testing")
    ])
def test_register_fail_invalid_json(email, username, password, bio, client):
    res = client.post(
        '/auth/register',
        json={"email": email, "username": username, "password": password, "bio": bio}
    )
    assert res.status_code == 422

def test_register_fail_user_exists(client, test_user_1):
    res = client.post(
        '/auth/register',
        json={
            "email": test_user_1["email"],
            "username": test_user_1["username"],
            "password": test_user_1["password"],
            "bio": test_user_1["bio"]
        })
    assert res.status_code == 403

def test_register_success(client, session):
    res = client.post(
        '/auth/register',
        json={"email": "testemail@gmail.com", "username": "test_user", "password": "asdfghjkl", "bio": "test"}
    )
    assert res.status_code == 200
    response = schemas.Token(**res.json())
    assert response.token_type == "bearer"
    payload = jwt.decode(response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    user_id_from_token = payload.get('id')
    user = session.query(models.User).filter(models.User.email == "testemail@gmail.com").first()
    assert user_id_from_token == user.userId

@pytest.mark.parametrize(
    "email, password", [
        ("testemail@gmail.com", None),
        (None, "123456789"),
        ("testemail", "123456789")
    ])
def test_login_fail_invalid_json(email, password, client, test_user_1):
    res = client.post(
        '/auth/login',
        json={"email": email, "password": password}
    )
    assert res.status_code == 422

@pytest.mark.parametrize(
    "email, password", [
        ("wrongemail@gmail.com", "123456789"),
        ("testemail@gmail.com", "wrong password"),
        ("wrongemail@gmail.com", "wrong password")
    ])
def test_login_fail_invalid_credentials(email, password, client, test_user_1):
    res = client.post(
        '/auth/login',
        json={"email": email, "password": password}
    )
    assert res.status_code == 404

def test_login_success(client, session, test_user_1):
    res = client.post(
        '/auth/login',
        json={"email": test_user_1["email"], "password": test_user_1["password"]}
    )
    assert res.status_code == 200
    response = schemas.Token(**res.json())
    assert response.token_type == "bearer"
    payload = jwt.decode(response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    user_id_from_token = payload.get('id')
    user = session.query(models.User).filter(models.User.email == "testemail@gmail.com").first()
    assert user_id_from_token == user.userId
