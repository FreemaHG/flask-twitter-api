import os

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api, reqparse
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from flasgger import APISpec, Swagger

from app.database import db
from app.settings import APP_SETTINGS
from app.schemas.base_response import ResponseSchema, ErrorResponseSchema
from app.schemas.users import UserOutSchema
from app.schemas.images import ImageResponseSchema
from app.schemas.tweets import TweetResponseSchema, TweetListSchema, TweetInSchema


MIGRATION_DIR = os.path.join("app", "migrations")  # Директория для миграций
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FOLDER = os.path.join(ROOT_DIR, "templates")
STATIC_FOLDER = os.path.join(ROOT_DIR, "static")

migrate = Migrate()


def create_app() -> Flask:
    """
    Функция создает и возвращает экземпляр приложения Flask
    """
    app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

    # app.config.from_object('config.DevelopmentConfig')
    app.config.from_object(
        APP_SETTINGS
    )  # Загружаем конфигурацию (подгруженную из .env) из файла настроек

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


def create_api(app: Flask) -> Api:
    """
    Функция возвращает экземпляр Flask RESTApi
    :param app: экземпляр Flask-приложения
    :return: экземпляр Flask RESTApi
    """
    # Оборачиваем api в swagger для автоматической документации (./api/spec.json)
    rest_api = Api(app, prefix="/api")

    parser = reqparse.RequestParser()
    parser.add_argument("api-key", location="headers")

    return rest_api


def create_swagger(app: Flask) -> Swagger:
    """
    Функция создает и возвращает экземпляр Swagger для формирования автоматической документации к RESTApi
    """

    # Инициализируем объект спецификации для приложения
    spec = APISpec(
        title='Twitter',  # Название спецификации
        version='1.0.0',  # Версия нашей спецификации
        openapi_version='2.0',  # Версия OpenAPI, которую мы будем использовать
        plugins=[  # Подключаемые плагины (расширяют функционал системы)
            FlaskPlugin(),  # Для быстрого добавления всех ендпоинтов в документацию
            MarshmallowPlugin(),
        ],
    )

    template = spec.to_flasgger(
        app,
        # Передаем схемы приложения
        definitions=[
            ResponseSchema,
            ErrorResponseSchema,
            UserOutSchema,
            ImageResponseSchema,
            TweetResponseSchema,
            TweetListSchema,
            TweetInSchema
        ],
    )

    swagger = Swagger(app, template=template)

    return swagger
