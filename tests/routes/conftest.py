import pytest
from http import HTTPStatus

from app.models.tweets import Tweet


@pytest.fixture
def tweets(db, users):
    """
    Твиты для тестирования
    """
    tweet_1 = Tweet(body='Тестовый твит 1', user_id=users[0].id)
    tweet_2 = Tweet(body='Тестовый твит 2', user_id=users[1].id)

    db.session.add_all([tweet_1, tweet_2])
    db.session.commit()

    return tweet_1, tweet_2


@pytest.fixture
def headers():
    """
    Параметр в header для выполнения запросов
    """
    return {'api-key': 'test-user1'}


@pytest.fixture
def good_response():
    """
    Успешный ответ
    """
    return {'result': True}


@pytest.fixture
def bad_response():
    """
    Неуспешный ответ
    """
    return {'result': False}


@pytest.fixture
def response_not_found(bad_response):
    """
    Ответ с кодом 404
    """
    bad_response['error_type'] = f'{HTTPStatus.NOT_FOUND}'
    return bad_response


@pytest.fixture
def response_locked(bad_response):
    """
    Ответ с кодом 423
    """
    bad_response['error_type'] = f'{HTTPStatus.LOCKED}'
    return bad_response


@pytest.fixture
def response_tweet_not_found(response_not_found):
    """
    Ответ с текстом ошибки, что твит не найден
    """
    response_not_found['error_message'] = 'Tweet not found'
    return response_not_found
