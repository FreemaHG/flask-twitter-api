import pytest

from app import create_app
from app.database import db as _db
from app.config import TestingConfig

# Импортируем все модели, чтобы все таблицы создавались в фикстуре db
from app.models.users import User
from app.models.tweets import Tweet, Image, Like


@pytest.fixture(scope="session")
def app():
    """
    Экземпляр приложения с тестовыми настройками
    """
    _app = create_app(app_settings=TestingConfig)
    yield _app


@pytest.fixture(scope="session")
def client(app):
    """
    Тестовый клиент для выполнения запросов
    """
    return app.test_client()


@pytest.fixture()
def db(app):
    """
    Создание и удаление БД для каждого теста
    """
    with app.app_context():
        # Создаем БД
        _db.create_all()

        yield _db

        # Закрываем сессию и удаляем БД
        _db.session.close()
        _db.drop_all()


@pytest.fixture(autouse=True)
def users(db):
    """
    Пользователи для тестирования
    """
    user_1 = User(name="test-user1", api_key="test-user1")
    user_2 = User(name="test-user2", api_key="test-user2")
    user_3 = User(name="test-user3", api_key="test-user3")

    db.session.add_all([user_1, user_2, user_3])
    db.session.commit()

    return user_1, user_2, user_3
