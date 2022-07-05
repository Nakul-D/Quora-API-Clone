import pytest
from app.routers.questions import schemas


def test_get_question_by_id_authorization_fail(client):
    res = client.get('/question/id/1')
    assert res.status_code == 401

def test_get_question_by_id_not_exists(authorized_client_1):
    res = authorized_client_1.get('/question/id/1000')
    assert res.status_code == 404

def test_get_question_by_id_success(authorized_client_1, create_test_questions):
    res = authorized_client_1.get(f'/question/id/{create_test_questions[0].questionId}')
    assert res.status_code == 200
    question = schemas.QuestionResponse(**res.json())
    assert question.userId == create_test_questions[0].userId
    assert question.question == create_test_questions[0].question
    assert question.questionId == create_test_questions[0].questionId

def test_get_question_by_search_authorization_fail(client):
    res = client.get('/question/search?keyword=test&limit=1')
    assert res.status_code == 401

def test_get_question_by_search_not_available(authorized_client_1, create_test_questions):
    res = authorized_client_1.get('/question/search?keyword=keywordDoesNotExists&limit=1')
    assert res.status_code == 200
    assert type(res.json()) == list
    assert len(res.json()) == 0

def test_get_question_by_search_success(authorized_client_1, create_test_questions):
    res = authorized_client_1.get('/question/search?keyword=test&limit=1')
    assert res.status_code == 200
    assert type(res.json()) == list
    assert len(res.json()) == 1
    question = schemas.QuestionResponse(**res.json()[0])
    assert question.userId == create_test_questions[0].userId
    assert question.question == create_test_questions[0].question
    assert question.questionId == create_test_questions[0].questionId

def test_post_question_authorization_fail(client):
    res = client.post(
        '/question/post',
        json={'question': 'posting test question'})
    assert res.status_code == 401

@pytest.mark.parametrize('key, value', [
    ('question', None),
    ('invalid_key', 'test_question')
])
def test_post_question_invalid_json_fail(key, value, authorized_client_1):
    res = authorized_client_1.post('/question/post', json={key: value})
    assert res.status_code == 422

def test_post_question_success(authorized_client_1, test_user_1):
    res = authorized_client_1.post('/question/post', json={'question': 'posting test question'})
    assert res.status_code == 201
    question = schemas.QuestionResponse(**res.json())
    assert question.userId == test_user_1['userId']
    assert question.question == 'posting test question'

def test_update_question_authorization_fail(client, create_test_questions):
    res = client.put(
        f'question/update/{create_test_questions[0].questionId}',
        json={'question': 'update question test'})
    assert res.status_code == 401

def test_update_question_not_found(authorized_client_1, create_test_questions):
    res = authorized_client_1.put(
        f'/question/update/1000',
        json={'question': 'question not found'})
    assert res.status_code == 404

@pytest.mark.parametrize('key, value', [
    ('question', None),
    ('invalid_key', 'test_question')
])
def test_update_question_invalid_json_fail(key, value, authorized_client_1, create_test_questions):
    res = authorized_client_1.put(
        f'/question/update/{create_test_questions[0].questionId}',
        json={key: value})
    assert res.status_code == 422

def test_update_other_users_question_fail(authorized_client_2, create_test_questions):
    res = authorized_client_2.put(
        f'question/update/{create_test_questions[0].questionId}',
        json={'question': 'update question test'})
    assert res.status_code == 403

def test_update_question_success(authorized_client_1, test_user_1, create_test_questions):
    res = authorized_client_1.put(
        f'/question/update/{create_test_questions[0].questionId}',
        json={'question': 'update_question_test'})
    assert res.status_code == 200
    question = schemas.QuestionResponse(**res.json())
    assert question.userId == test_user_1['userId']
    assert question.question == 'update_question_test'
    assert question.edited == True

def test_delete_question_authorization_fail(client, create_test_questions):
    res = client.delete(f'/question/delete/{create_test_questions[0].questionId}')
    assert res.status_code == 401

def test_delete_question_not_found_fail(authorized_client_1, create_test_questions):
    res = authorized_client_1.delete(f'/question/delete/1000')
    assert res.status_code == 404

def test_delete_other_users_question_fail(authorized_client_2, create_test_questions):
    res = authorized_client_2.delete(f'/question/delete/{create_test_questions[0].questionId}')
    assert res.status_code == 403

def test_delete_question_success(authorized_client_1, create_test_questions):
    res = authorized_client_1.delete(f'/question/delete/{create_test_questions[0].questionId}')
    assert res.status_code == 204
