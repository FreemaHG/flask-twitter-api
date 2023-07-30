from http import HTTPStatus

from app.tests.conftest import app, client, db


def test_user_me_data(client) -> None:
    """
    Тестирование ендпоинта по выводу данных о текущем пользователе
    """
    resp = client.get('/api/users/me', headers={'api-key': 'test-user1'})

    await_response = {
        'result': True,
        'user': {
            'id': 1,
            'name': 'test-user1',
            'following': [{'id': 2, 'name': 'test-user2'}],
            'followers': [{'id': 2, 'name': 'test-user2'}],
        },
    }

    assert resp.status_code == HTTPStatus.OK
    assert resp.json == await_response


def test_user_data_for_id(client) -> None:
    """
    Тестирование ендпоинта по выводу данных о пользователе по переданному id
    """
    resp = client.get('/api/users/2', headers={'api-key': 'test-user1'})

    await_response = {
        'result': True,
        'user': {
            'id': 2,
            'name': 'test-user2',
            'following': [{'id': 1, 'name': 'test-user1'}],
            'followers': [{'id': 1, 'name': 'test-user1'}],
        },
    }

    assert resp.status_code == HTTPStatus.OK
    assert resp.json == await_response


def test_user_data_for_id_not_found(client) -> None:
    """
    Тестирование вывода ошибки при отсутствии пользователя по переданному id
    """
    resp = client.get('/api/users/1000', headers={'api-key': 'test-user1'})

    await_response = {
        'result': False,
        'error_type': f'{HTTPStatus.NOT_FOUND}',
        'error_message': 'Sorry. This user does not exist'
    }

    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert resp.json == await_response
