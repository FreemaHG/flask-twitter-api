import json
from http import HTTPStatus

from app.tests.conftest import app, client, db


def test_create_tweet(client) -> None:
    """
    Тестирование добавления твита (без изображений)
    """

    new_tweet = {'tweet_data': 'Тестовый твит', 'tweet_media_ids': []}

    resp = client.post(
        '/api/tweets',
        data=json.dumps(new_tweet),
        headers={'api-key': 'test-user1', 'Content-Type': 'application/json'}
    )

    await_response = {'result': True, 'tweet_id': 4}

    assert resp.status_code == HTTPStatus.CREATED
    assert resp.json == await_response


def test_create_tweet_with_images(client) -> None:
    """
    Тестирование добавления твита с изображениями
    """

    new_tweet = {'tweet_data': 'Тестовый твит', 'tweet_media_ids': [1, 2]}

    resp = client.post(
        '/api/tweets',
        data=json.dumps(new_tweet),
        headers={'api-key': 'test-user1', 'Content-Type': 'application/json'}
    )

    await_response = {'result': True, 'tweet_id': 4}

    assert resp.status_code == HTTPStatus.CREATED
    assert resp.json == await_response


def test_create_invalid_tweet(client) -> None:
    """
    Тестирование вывода сообщения об ошибке при публикации слишком длинного твита (> 280 символов)
    """

    new_tweet = {
        'tweet_data': 'Python — идеальный язык для новичка. '
                      'Код на Python легко писать и читать, язык стабильно занимает высокие места '
                      'в рейтингах популярности, а «питонисты» востребованы почти во всех сферах '
                      'IT — программировании, анализе данных, системном администрировании и тестировании. '
                      'YouTube, Intel, Pixar, NASA, VK, Яндекс — вот лишь немногие из известных компаний, '
                      'которые используют Python в своих продуктах.',
        'tweet_media_ids': []
    }

    resp = client.post(
        '/api/tweets',
        data=json.dumps(new_tweet),
        headers={'api-key': 'test-user1', 'Content-Type': 'application/json'}
    )

    await_response = {
        'result': False,
        'error_type': f'{HTTPStatus.BAD_REQUEST}',
        'error_message': 'The length of the tweet should not exceed 280 characters. '
                         f'Current value: {len(new_tweet["tweet_data"])}'
    }

    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert resp.json == await_response


def test_delete_tweet(client) -> None:
    """
    Тестирование удаление твита
    """
    resp = client.delete('/api/tweets/3', headers={'api-key': 'test-user1'})
    await_response = {'result': True}

    assert resp.status_code == HTTPStatus.OK
    assert resp.json == await_response


def test_delete_tweet_not_found(client) -> None:
    """
    Тестирование вывода ошибки при попытке удалить несуществующий твит
    """
    resp = client.delete('/api/tweets/1000', headers={'api-key': 'test-user1'})

    await_response = {
        'result': False,
        'error_type': f'{HTTPStatus.NOT_FOUND}',
        'error_message': 'Tweet not found'
    }

    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert resp.json == await_response


def test_delete_tweet_locked(client) -> None:
    """
    Тестирование вывода ошибки при попытке удалить чужой твит
    """
    resp = client.delete('/api/tweets/2', headers={'api-key': 'test-user1'})

    await_response = {
        'result': False,
        'error_type': f'{HTTPStatus.LOCKED}',
        'error_message': 'The tweet that is being accessed is locked'
    }

    assert resp.status_code == HTTPStatus.LOCKED
    assert resp.json == await_response
