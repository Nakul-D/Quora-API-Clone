import pytest


def test_vote_authorization_fail(client, create_test_answers):
    res = client.post(
        f"/vote/{create_test_answers[0].answerId}",
        json={'upvoted': True})
    assert res.status_code == 401

@pytest.mark.parametrize('key, value', [
    ('wrong_key', True),
    ('upvoted', 'wrong_value')])
def test_vote_fail_invalid_json(key, value, authorized_client_1, create_test_answers):
    res = authorized_client_1.post(
        f"/vote/{create_test_answers[0].answerId}",
        json={key: value})
    assert res.status_code == 422

def test_vote_fail_answer_does_not_exist(authorized_client_1):
    res = authorized_client_1.post(f"/vote/1", json={'upvoted': True})
    assert res.status_code == 404

def test_add_vote(authorized_client_1, create_test_answers):
    res = authorized_client_1.post(
        f"/vote/{create_test_answers[0].answerId}",
        json={'upvoted': True})
    assert res.status_code == 201

def test_update_vote(authorized_client_1, create_test_vote):
    res = authorized_client_1.post(
        f"/vote/{create_test_vote.answerId}",
        json={'upvoted': not create_test_vote.vote})
    assert res.status_code == 200

def test_delete_vote(authorized_client_1, create_test_vote):
    res = authorized_client_1.post(
        f"/vote/{create_test_vote.answerId}",
        json={'upvoted': create_test_vote.vote})
    assert res.status_code == 204
