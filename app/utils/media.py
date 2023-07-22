import os

from flask import current_app
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from loguru import logger

# from ..main import app


def allowed_image(image_name: str) -> bool:
    """
    Функция проверяет расширение изображения и возвращает True, если формат разрешен
    :param image_name: название изображения
    :return: True - формат разрешен / иначе False
    """
    with current_app.app_context():
        _allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']

    # .rsplit('.', 1) - делит строку, начиная справа; 1 - делит 1 раз (по умолчанию -1 - неограниченное кол-во раз)
    return '.' in image_name and image_name.rsplit('.', 1)[1].lower() in _allowed_extensions


def path_avatar(path: str) -> str:
    """
    Функция возвращает очищенную строку-путь без папки static
    :param path: строка - полный путь
    :return: очищенная строка
    """
    return path.split('static')[1]


def save_image(image: FileStorage, avatar=False) -> str:
    """
    Функция сохраняет переданное изображение
    :param avatar: переключатель для сохранения аватара или изображения к твиту
    :param image: изображение
    :return: путь относительно static для сохранения в БД
    """
    with current_app.app_context():
        _upload_folder = os.path.join(current_app.config['UPLOAD'])

    filename = secure_filename(image.filename)  # Проверяем файл для безопасности

    if avatar:
        logger.debug('Сохранение аватара пользователя')
        path = os.path.join(_upload_folder, 'avatars', filename)

    else:
        logger.debug('Сохранение изображения к твиту')
        path = os.path.join(_upload_folder, 'tweets', filename)

    try:
        image.save(path)

    except FileNotFoundError:
        new_path = path.rsplit('/', 1)[0].rsplit('\\', 1)[0]
        logger.warning(f'Создание директории: {new_path}')

        # Создание нескольких вложенных папок
        os.makedirs(new_path)
        image.save(path)

    path = path_avatar(path)

    return path
