import os

from dotenv import load_dotenv, find_dotenv

# Функция find_dotenv возвращает путь к файлу .env, если такой есть
if not find_dotenv():
    # Если файла с настройками бота нет, завершается работа python с соответствующим сообщением
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

APP_SETTINGS = os.getenv('APP_SETTINGS')  # Сохраняем выбранную конфигурацию для использования в приложении
