import pytest
from app.database.models import Answer


def test_get_answer_by_id_authorization_fail(client, create_test_answers):
    res = client.get(f"/answer/id/{create_test_answers[0].answerId}")
    assert res.status_code == 401

def test_get_answer_by_id_fail_not_exists(authorized_client_1, create_test_answers):
    res = authorized_client_1.get('/answer/id/1000')
    assert res.status_code == 404

def test_get_answer_by_id(authorized_client_1, create_test_answers):
    res = authorized_client_1.get(f"/answer/id/{create_test_answers[0].answerId}")
    assert res.status_code == 200
    answer = Answer(**res.json())
    assert answer.userId == create_test_answers[0].userId
    assert answer.answerId == create_test_answers[0].answerId
    assert answer.answer == create_test_answers[0].answer
    assert answer.questionId == create_test_answers[0].questionId

def test_post_answer_authorization_fail(client, create_test_questions):
    res = client.post(
        f"/answer/post/{create_test_questions[0].questionId}",
        json={'answer': 'posting test answer'})
    assert res.status_code == 401

@pytest.mark.parametrize(
    'key, value', [
    ('answer', None),
    ('invalid_key', 'test_question')])
def test_post_answer_fail_invalid_json(key, value, authorized_client_1, create_test_questions):
    res = authorized_client_1.post(
        f"/answer/post/{create_test_questions[0].questionId}",
        json={key: value})
    assert res.status_code == 422

def test_post_answer_fail_question_does_not_exist(authorized_client_1):
    res = authorized_client_1.post('/answer/post/1', json={'answer': 'test answer'})
    assert res.status_code == 404

def test_post_answer_fail_already_answered(authorized_client_1, create_test_answers):
    res = authorized_client_1.post(
        f"/answer/post/{create_test_answers[0].questionId}",
        json={'answer': 'test answer'})
    assert res.status_code == 406

def test_post_answer(test_user_1, authorized_client_1, create_test_questions):
    questionId = create_test_questions[0].questionId
    res = authorized_client_1.post(
        f"/answer/post/{questionId}",
        json={'answer': 'test answer'})
    assert res.status_code == 201
    answer = Answer(**res.json())
    assert answer.userId == test_user_1['userId']
    assert answer.questionId == questionId
    assert answer.answer == 'test answer'
    assert answer.edited == False

def test_update_answer_authorization_fail(client, create_test_answers):
    res = client.put(
        f"answer/update/{create_test_answers[0].answerId}",
        json={'answer': 'updated_answer'})   
    assert res.status_code == 401

@pytest.mark.parametrize('key, value', [
    ('answer', None),
    ('invalid_key', 'test_answer')])
def test_update_answer_fail_invalid_json(key, value, authorized_client_1, create_test_answers):
    res = authorized_client_1.put(
        f"answer/update/{create_test_answers[0].answerId}",
        json={key: value})
    assert res.status_code == 422

def test_update_answer_fail_answer_does_not_exist(authorized_client_1):
    res = authorized_client_1.put('answer/update/1', json={'answer': 'updated_answer'})
    assert res.status_code == 404

def test_update_answer_fail_cant_update_other_users_answer(authorized_client_2, create_test_answers):
    res = authorized_client_2.put(
        f"answer/update/{create_test_answers[0].answerId}",
        json={'answer': 'updated_answer'})
    assert res.status_code == 403

def test_update_answer(test_user_1, authorized_client_1, create_test_answers):
    res = authorized_client_1.put(
        f"answer/update/{create_test_answers[0].answerId}",
        json={'answer': 'updated_answer'})
    assert res.status_code == 200
    answer = Answer(**res.json())
    assert answer.userId == test_user_1['userId']
    assert answer.questionId == create_test_answers[0].questionId
    assert answer.answer == 'updated_answer'
    assert answer.edited == True

def test_delete_answer_authorization_fail(client, create_test_answers):
    res = client.delete(f"answer/delete/{create_test_answers[0].answerId}")
    assert res.status_code == 401

def test_delete_answer_fail_answer_does_not_exist(authorized_client_1):
    res = authorized_client_1.delete(f"answer/delete/1")
    assert res.status_code == 404

def test_delete_answer_fail_cant_delete_other_users_answer(authorized_client_2, create_test_answers):
    res = authorized_client_2.delete(f"answer/delete/{create_test_answers[0].answerId}")
    assert res.status_code == 403

def test_delete_answer(authorized_client_1, create_test_answers):
    res = authorized_client_1.delete(f"answer/delete/{create_test_answers[0].answerId}")
    assert res.status_code == 204
