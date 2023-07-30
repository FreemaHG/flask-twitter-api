import os.path

import pytest

from pathlib import Path

from app import create_app
from app.database import db as _db
from app.models.users import User
from app.config import TestingConfig
from app.models.tweets import Tweet, Like, Image


@pytest.fixture
def app():
    # Создаем экземпляр приложения с настройками для тестирования
    _app = create_app(app_settings=TestingConfig)

    with _app.app_context():
        _db.create_all()

        # Тестовые данные
        # Пользователи
        test_user1 = User(name='test-user1', api_key='test-user1')
        test_user2 = User(name='test-user2', api_key='test-user2')
        test_user3 = User(name='test-user3', api_key='test-user3')

        # Подписки
        test_user1.following.append(test_user2)
        test_user2.following.append(test_user1)

        # Твиты
        tweet1 = Tweet(body='1 тестовый твит', user=test_user1)
        tweet2 = Tweet(body='2 тестовый твит', user=test_user2)
        tweet3 = Tweet(body='3 тестовый твит', user=test_user1)

        # Изображения
        image1 = Image(tweet_id=tweet1.id, path=os.path.join('files_for_tests', 'test_image.jpg'))
        image2 = Image(tweet_id=tweet2.id, path=os.path.join('files_for_tests', 'test_image.jpg'))
        tweet1.images.append(image1)
        tweet2.images.append(image2)

        # Лайки
        like1 = Like(user=test_user1, tweet=tweet1)
        like2 = Like(user=test_user2, tweet=tweet2)

        _db.session.add_all([test_user1, test_user2, test_user3, tweet1, tweet2, tweet3, like1, like2])
        _db.session.commit()

        yield _app

        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    """
    Тестовый клиент для выполнения запросов
    """
    client = app.test_client()

    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
