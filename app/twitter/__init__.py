import os
from loguru import logger

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api

from .database import db
from .settings import APP_SETTINGS


_MIGRATION_DIR = os.path.join('app', 'twitter/migrations')  # Директория для миграций


def create_app():
    """
    Функция, отвечающая за создание экземпляра приложения
    """
    app = Flask(__name__)

    # Работает
    # app.config.from_object('config.DevelopmentConfig')
    app.config.from_object(APP_SETTINGS)  # Загружаем конфигурацию (подгруженную из .env) из файла настроек

    # Инициализация БД
    db.init_app(app)

    migrate = Migrate()
    # ma = Marshmallow(app)  # TODO В работе

    # Инициализация репозитория для миграций в корне проекта
    migrate.init_app(app, db, directory=_MIGRATION_DIR, render_as_batch=True)

    api = Api(app)

    # Импортируем все модели перед инициализацией БД
    from .users.models import User

    # Создание БД
    with app.test_request_context():
        db.create_all()

    from .users.routes import UserData

    api.add_resource(UserData, '/api/users/me', endpoint='personal-data')

    return app
