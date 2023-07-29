import os

from dotenv import load_dotenv, find_dotenv


# Функция find_dotenv возвращает путь к файлу .env, если такой есть
if not find_dotenv():
    # Завершение работы с соответствующим сообщением, если .env нет
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()  # Загрузка переменных окружения

# Сохраняем выбранную конфигурацию из config.py для использования в приложении
APP_SETTINGS = os.getenv("APP_SETTINGS")
