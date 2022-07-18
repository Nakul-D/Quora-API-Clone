import pytest
from app.routers.user import schemas


def test_get_user_by_id_authorization_fail(client):
    res = client.get('/user/1')
    assert res.status_code == 401

def test_get_user_by_id_does_not_exist(authorized_client_1):
    res = authorized_client_1.get('/user/1000')
    assert res.status_code == 404

def test_get_user_by_id(test_user_1, authorized_client_1, create_test_questions, create_test_answers, create_test_vote):
    userId = test_user_1["userId"]
    res = authorized_client_1.get(f"/user/{userId}")
    assert res.status_code == 200
    profile: schemas.UserProfileResponse = schemas.UserProfileResponse(**res.json())
    assert profile.userId == userId
    assert profile.username == test_user_1["username"]
    assert profile.bio == test_user_1["bio"]
    assert len(profile.questions) == 2
    for question in profile.questions:
        assert question.userId == userId
    assert len(profile.answers) == 2
    for answer in profile.answers:
        assert answer.answer.userId == userId
    assert profile.answers[0].answer.upVotes == 1

def test_update_bio_authorization_fail(client):
    res = client.post('/user/updateBio', json={'newBio': 'updated bio'})
    assert res.status_code == 401

@pytest.mark.parametrize('key, value', [
    ('invalid_key', 'updated_bio'),
    ('newBio', None)
])
def test_update_bio_invalid_json_fail(key, value, authorized_client_1):
    res = authorized_client_1.post('/user/updateBio', json={key: value})
    assert res.status_code == 422

def test_update_bio(authorized_client_1):
    res = authorized_client_1.post('/user/updateBio', json={'newBio': 'updated bio'})
    assert res.status_code == 200
