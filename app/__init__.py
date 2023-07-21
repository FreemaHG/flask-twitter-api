import os
from loguru import logger

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api, reqparse

from .database import db
from .settings import APP_SETTINGS


MIGRATION_DIR = os.path.join('app', 'migrations')  # Директория для миграций
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FOLDER = os.path.join(ROOT_DIR, 'templates')
STATIC_FOLDER = os.path.join(ROOT_DIR, 'static')

migrate = Migrate()


def create_app():
    """
    Функция, отвечающая за создание экземпляра приложения
    """
    app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

    # app.config.from_object('config.DevelopmentConfig')
    app.config.from_object(APP_SETTINGS)  # Загружаем конфигурацию (подгруженную из .env) из файла настроек

    # Инициализация БД
    db.init_app(app)

    # migrate = Migrate(app, db)

    # Инициализация репозитория для миграций в корне проекта
    migrate.init_app(app, db, directory=MIGRATION_DIR, render_as_batch=True)

    # Импортируем все модели перед инициализацией БД
    from .models.users import User
    from .models.tweets import Tweet, Tag, Image, Like, Comment

    # Создание БД
    with app.test_request_context():
        db.create_all()

    return app


def create_api(app):
    """
    Функция, отвечающая за создание экземпляра rest_api
    """
    rest_api = Api(app)

    parser = reqparse.RequestParser()
    parser.add_argument('api-key', location='headers')

    return rest_api
