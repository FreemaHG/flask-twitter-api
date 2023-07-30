from http import HTTPStatus

from app.tests.conftest import app, client, db


def test_create_follower(client) -> None:
    """
    Тестирование подписки на пользователя
    """
    resp = client.post('/api/users/3/follow', headers={'api-key': 'test-user1'})
    await_response = {'result': True}

    assert resp.status_code == HTTPStatus.CREATED
    assert resp.json == await_response


def test_create_follower_not_found(client) -> None:
    """
    Тестирование вывода ошибки при попытке подписки на несуществующего пользователя
    """
    resp = client.post('/api/users/1000/follow', headers={'api-key': 'test-user1'})
    await_response = {
        'result': False,
        'error_type': f'{HTTPStatus.NOT_FOUND}',
        'error_message': 'The subscription user was not found'
    }

    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert resp.json == await_response


def test_create_follower_locked(client) -> None:
    """
    Тестирование вывода ошибки при попытке подписки на уже подписанного ранее пользователя
    """
    resp = client.post('/api/users/2/follow', headers={'api-key': 'test-user1'})
    await_response = {
        'result': False,
        'error_type': f'{HTTPStatus.LOCKED}',
        'error_message': 'The subscription has already been issued'
    }

    assert resp.status_code == HTTPStatus.LOCKED
    assert resp.json == await_response


def test_delete_follower(client) -> None:
    """
    Тестирование удаления подписки пользователя
    """
    resp = client.delete('/api/users/2/follow', headers={'api-key': 'test-user1'})
    await_response = {'result': True}

    assert resp.status_code == HTTPStatus.OK
    assert resp.json == await_response


def test_delete_follower_not_found(client) -> None:
    """
    Тестирование вывода ошибки при удалении подписки с несуществующего пользователя
    """
    resp = client.delete('/api/users/1000/follow', headers={'api-key': 'test-user1'})
    await_response = {
        'result': False,
        'error_type': f'{HTTPStatus.NOT_FOUND}',
        'error_message': 'The user to cancel the subscription was not found'
    }

    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert resp.json == await_response


def test_delete_follower_locked(client) -> None:
    """
    Тестирование вывода ошибки при удалении подписки от пользователя, на которого нет подписки
    """
    resp = client.delete('/api/users/3/follow', headers={'api-key': 'test-user1'})
    await_response = {
        'result': False,
        'error_type': f'{HTTPStatus.LOCKED}',
        'error_message': 'The user is not among the subscribers'
    }

    assert resp.status_code == HTTPStatus.LOCKED
    assert resp.json == await_response
