from http import HTTPStatus

from app.tests.conftest import app, client, db


def test_create_like(client) -> None:
    """
    Тестирование добавления лайка к твиту
    """
    resp = client.post('/api/tweets/2/likes', headers={'api-key': 'test-user1'})
    await_response = {'result': True}

    assert resp.status_code == HTTPStatus.CREATED
    assert resp.json == await_response


def test_create_like_not_found(client) -> None:
    """
    Тестирование вывода ошибки при попытке поставить лайк несуществующему твиту
    """
    resp = client.post('/api/tweets/1000/likes', headers={'api-key': 'test-user1'})
    await_response = {
        'result': False,
        'error_type': f'{HTTPStatus.NOT_FOUND}',
        'error_message': 'Tweet not found'
    }

    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert resp.json == await_response


def test_create_like_locked(client) -> None:
    """
    Тестирование вывода ошибки при добавлении лайка твиту, у которого уже есть лайк от пользователя
    """
    resp = client.post('/api/tweets/1/likes', headers={'api-key': 'test-user1'})
    await_response = {
        'result': False,
        'error_type': f'{HTTPStatus.LOCKED}',
        'error_message': 'The user has already liked this tweet'
    }

    assert resp.status_code == HTTPStatus.LOCKED
    assert resp.json == await_response


def test_delete_like(client) -> None:
    """
    Тестирование удаления лайка
    """
    resp = client.delete('/api/tweets/1/likes', headers={'api-key': 'test-user1'})
    await_response = {'result': True}

    assert resp.status_code == HTTPStatus.OK
    assert resp.json == await_response


def test_delete_like_not_found(client) -> None:
    """
    Тестирование вывода ошибки при удалении лайка у несуществующей записи
    """
    resp = client.delete('/api/tweets/1000/likes', headers={'api-key': 'test-user1'})
    await_response = {
        'result': False,
        'error_type': f'{HTTPStatus.NOT_FOUND}',
        'error_message': 'Tweet not found'
    }

    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert resp.json == await_response


def test_delete_like_locked(client) -> None:
    """
    Тестирование вывода ошибки при попытке удалить не существующий лайк
    """
    resp = client.delete('/api/tweets/3/likes', headers={'api-key': 'test-user1'})
    await_response = {
        'result': False,
        'error_type': f'{HTTPStatus.LOCKED}',
        'error_message': 'The user has not yet liked this tweet'
    }

    assert resp.status_code == HTTPStatus.LOCKED
    assert resp.json == await_response
