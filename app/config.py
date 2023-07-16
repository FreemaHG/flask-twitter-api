import os


_IMAGES_FOLDER = os.path.join('twitter/static', 'img')  # Директория для аватаров и изображений к твитам


class Config(object):
    """
    Базовая конфигурация приложения
    """
    DEBUG = False  # Режим разработки (вывод всех логов и ошибок)
    CSRF_ENABLED = True  # Включение защиты против "Cross-site Request Forgery (CSRF)"
    SECRET_KEY = 'dev'  # Секретный ключ, н-р, для подписи cookie
    SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'  # Местоположение БД
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Отключаем систему событий Flask-SQLAlchemy


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.urandom(32)  # Генерируем случайный ключ


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    UPLOAD = _IMAGES_FOLDER


class TestingConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
