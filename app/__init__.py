import os
from typing import Dict

from flask import Flask
# from flask_migrate import Migrate
from flask_restful import Api, reqparse
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from flasgger import APISpec, Swagger

from app.database import db
from app.utils.settings import get_settings
from app.schemas.base_response import ResponseSchema, ErrorResponseSchema
from app.schemas.users import UserOutSchema
from app.schemas.images import ImageResponseSchema
from app.schemas.tweets import TweetResponseSchema, TweetListSchema, TweetInSchema
from app.urls import add_urls
from app.utils.settings import get_settings


# MIGRATION_DIR = os.path.join("app", "../migrations")  # Директория для миграций
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FOLDER = os.path.join(ROOT_DIR, "templates")
STATIC_FOLDER = os.path.join(ROOT_DIR, "static")

# migrate = Migrate()


def create_app(app_settings=None) -> Flask:
    """
    Функция создает и возвращает экземпляр приложения Flask
    """

    if not app_settings:
        app_settings = get_settings()

    app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

    # Загружаем конфигурацию приложения (указанную в .env)
    app.config.from_object(app_settings)

    # Создаем репозиторий для миграций в корне проекта при разработке
    # dev_settings = app.config.get('DEVELOPMENT', None)

    # if dev_settings:
    #     app = migrate_start(app=app)

    # Инициализация БД
    db.init_app(app)

    # Импортируем все модели перед инициализацией БД
    from app.models.users import User
    from app.models.tweets import Tweet, Image, Like

    # Создание БД
    with app.test_request_context():
        db.create_all()

    rest_api = create_api(app)  # Экземпляр Flask RESTApi
    add_urls(rest_api)  # Регистрация URL
    create_swagger(app=app)  # Подключаем Swagger для автоматической документации

    return app

#
# def migrate_start(app: Flask) -> Flask:
#     """
#     Функция для запуска инициализации репозитория для миграций в корне проекта
#     :param app: экземпляр Flask-приложения
#     :return: None
#     """
#     migrate = Migrate()
#
#     # Инициализация репозитория для миграций в корне проекта
#     migrate.init_app(app, db, directory=MIGRATION_DIR, render_as_batch=True)
#
#     return app


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
