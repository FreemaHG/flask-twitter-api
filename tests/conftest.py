import pytest

from app import create_app
from app.database import db as _db
from app.config import TestingConfig


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
