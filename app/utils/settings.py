import os

from dotenv import load_dotenv, find_dotenv

load_dotenv()  # Загрузка переменных окружения

# Переменные окружения для подключения к PostgresSQL
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

APP_SETTINGS = os.environ.get("APP_SETTINGS")

#
# def get_settings():
#     """
#     Функция возвращает настройки приложения для разработки, тестирования и продакшена
#     в зависимости от указанных в .env конфигах
#     """
#
#     # Функция find_dotenv возвращает путь к файлу .env, если такой есть
#     if not find_dotenv():
#         # Завершение работы с соответствующим сообщением, если .env нет
#         exit("Переменные окружения не загружены т.к отсутствует файл .env")
#     else:
#         load_dotenv()  # Загрузка переменных окружения
#
#     # Сохраняем выбранную конфигурацию из config.py для использования в приложении
#     return os.getenv("APP_SETTINGS")
