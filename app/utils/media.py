import os

from datetime import datetime
from itertools import chain
from flask import current_app
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from loguru import logger

from ..database import db
from ..models.tweets import Image


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


def clear_path(path: str) -> str:
    """
    Функция возвращает очищенную строку-путь без папки static
    :param path: строка - полный путь
    :return: очищенная строка
    """
    return path.split('static')[1][1:]


def save_image(image: FileStorage, avatar=False) -> str:
    """
    Функция сохраняет переданное изображение
    :param avatar: переключатель для сохранения аватара или изображения к твиту
    :param image: изображение
    :return: путь относительно static для сохранения в БД
    """

    with current_app.app_context():
        _upload_folder = current_app.config['UPLOAD']

    filename = secure_filename(image.filename)  # Проверяем файл для безопасности

    if avatar:
        logger.debug('Сохранение аватара пользователя')
        path = os.path.join(_upload_folder, 'avatars', filename)

    else:
        logger.debug('Сохранение изображения к твиту')

        # Сохраняем изображения в директорию по дате добавления твита
        current_date = datetime.now()
        path = os.path.join(
            _upload_folder, 'tweets', f'{current_date.year}', f'{current_date.month}', f'{current_date.day}', filename
        )

    try:
        image.save(path)

    except FileNotFoundError:
        new_path = path.rsplit('/', 1)[0].rsplit('\\', 1)[0]
        logger.warning(f'Создание директории: {new_path}')

        # Создание нескольких вложенных папок
        os.makedirs(new_path)
        image.save(path)

    path = clear_path(path)

    return path


def delete_image(tweet_id: int) -> None:
    """
    Функция удаляет из файловой системы изображения по переданному id твита
    :param tweet_id: id твита
    :return: None
    """
    logger.debug(f'Удаление изображений к твиту №{tweet_id}')

    images = db.session.execute(db.select(Image).filter(Image.tweet_id == tweet_id)).all()

    if images:
        images = list(chain(*images))
        # Директория с изображениями к твиту
        folder = os.path.join('static', images[0].path.rsplit('/', 1)[0].rsplit('\\', 1)[0])

        for img in images:
            try:
                os.remove(os.path.join('static', img.path))

            except FileNotFoundError:
                logger.error(f'Директория: {img.path} не найдена')

        logger.info('Все изображения удалены')

        check_and_delete_folder(path=folder)  # Проверка и очистка директории, если пустая

    else:
        logger.warning('Изображения не найдены')


def check_and_delete_folder(path: str) -> None:
    """
    Функция проверяет и удаляет папку, если она пуста (подчистка пустых директорий после удалений твитов)
    :param path: директория с изображениями после удаления твита
    :return: None
    """
    try:
        if len(os.listdir(path)) == 0:
            os.rmdir(path)
            logger.info(f'Директория: {path} удалена')

    except FileNotFoundError:
        logger.error(f'Директория: {path} не найдена')
