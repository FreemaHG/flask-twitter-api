import os

from app.utils.settings import DB_USER, DB_PASS, DB_PORT, DB_NAME, DB_HOST


_IMAGES_FOLDER = os.path.join(
    "static", "img"
)  # Директория для аватаров и изображений к твитам

class Config(object):
    """
    Базовая конфигурация приложения
    """
    DEBUG = False  # Режим разработки (вывод всех логов и ошибок)
    CSRF_ENABLED = True  # Включение защиты против "Cross-site Request Forgery (CSRF)"
    SECRET_KEY = "dev"  # Секретный ключ, н-р, для подписи cookie
    SQLALCHEMY_DATABASE_URI = "sqlite:///project.db"  # Местоположение БД
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Отключаем систему событий Flask-SQLAlchemy
    UPLOAD = _IMAGES_FOLDER  # Директория для загрузки файлов
    # Разрешенные форматы для загрузки изображений
    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "gif",
    }

class DevelopmentConfig(Config):
    """
    Конфигурация для разработки
    """
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class TestingConfig(Config):
    """
    Конфигурация для тестирования
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Создаем тестовую БД в памяти (не в файле)

class ProductionConfig(DevelopmentConfig):
    """
    Конфигурация для рабочей среды
    """
    DEBUG = False
    SECRET_KEY = os.urandom(32)  # Генерируем ключ
