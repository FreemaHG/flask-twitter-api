import os


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


class ProductionConfig(Config):
    """
    Конфигурация для рабочей среды
    """

    DEBUG = False
    SECRET_KEY = os.urandom(32)  # Генерируем случайный ключ


class DevelopmentConfig(Config):
    """
    Конфигурация для разработки
    """

    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """
    Конфигурация для тестирования
    """

    DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
