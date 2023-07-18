import os
from loguru import logger

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from .database import db
from .settings import APP_SETTINGS


_MIGRATION_DIR = os.path.join('app', 'migrations')  # Директория для миграций
_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
_TEMPLATE_FOLDER = os.path.join(_ROOT_DIR, '/templates')
_STATIC_FOLDER = os.path.join(_ROOT_DIR, '/static')

migrate = Migrate()


def create_app():
    """
    Функция, отвечающая за создание экземпляра приложения
    """
    app = Flask(__name__, template_folder=_TEMPLATE_FOLDER, static_folder=_STATIC_FOLDER)

    # app.config.from_object('config.DevelopmentConfig')
    app.config.from_object(APP_SETTINGS)  # Загружаем конфигурацию (подгруженную из .env) из файла настроек

    # Инициализация БД
    db.init_app(app)

    # migrate = Migrate(app, db)

    # Инициализация репозитория для миграций в корне проекта
    migrate.init_app(app, db, directory=_MIGRATION_DIR, render_as_batch=True)

    api = Api(app)

    # Импортируем все модели перед инициализацией БД
    from .models.users import User
    from .models.tweets import Tweet, Tag, Image, Like, Comment

    # Создание БД
    with app.test_request_context():
        db.create_all()

    from .routes.users import UserData, UserDataForId

    api.add_resource(UserData, '/api/users/me', endpoint='personal-data')
    api.add_resource(UserDataForId, '/api/users/<int:user_id>', endpoint='user-data')

    return app
