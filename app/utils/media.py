import os

from flask import current_app
from werkzeug.utils import secure_filename


_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Разрешенные форматы изображений для загрузки
_AVATARS_FOLDER = os.path.join(current_app.config['UPLOAD'], 'avatars')


def allowed_image(image_name: str) -> bool:
    """
    Функция проверяет расширение изображения и возвращает True, если формат разрешен
    :param image_name: название изображения
    :return: True/False
    """
    # .rsplit('.', 1) - делит строку, начиная справа; 1 - делит 1 раз (по умолчанию -1 - неограниченное кол-во раз)
    return '.' in image_name and image_name.rsplit('.', 1)[1].lower() in _ALLOWED_EXTENSIONS


def path_avatar(path: str) -> str:
    """
    Функция возвращает очищенную строку-путь без папки static
    :param path: строка - полный путь
    :return: очищенная строка
    """
    return path.split('/static')[1]


def save_avatar(file) -> str:
    """
    Функция сохраняет переданное изображение
    :param file: аватар
    :return: путь относительно static для сохранения в БД
    """
    filename = secure_filename(file.filename)  # Проверяем файл для безопасности
    path = os.path.join(_AVATARS_FOLDER, filename)
    file.save(path)

    path = path_avatar(path)

    return path
