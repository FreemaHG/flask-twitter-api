import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Папка для хранения миграций
MIGRATION_DIR = os.path.join('app', 'migrations')
IMAGES_FOLDER = os.path.join('static', 'img')

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    """
    Функция, отвечающая за создание экземпляра приложения
    """

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',  # FIXME Обязательно изменить после завершения разработки API
        SQLALCHEMY_DATABASE_URI='sqlite:///project.db',
        UPLOAD=IMAGES_FOLDER,  # Для загрузки изображений (аватары и изображения к твитам)
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)  # Инициализация БД
    migrate.init_app(app, db, directory=MIGRATION_DIR)  # Инициализация репозитория для миграций в корне проекта

    # Импортируем все модели перед инициализацией БД
    from .models.user import User

    # Создание БД
    with app.app_context():
        db.create_all()

    return app
