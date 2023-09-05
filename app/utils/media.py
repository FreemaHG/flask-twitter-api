import os

from datetime import datetime
from itertools import chain
from flask import current_app
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from loguru import logger

from app.database import db
from app.models.tweets import Image


def allowed_image(image_name: str) -> bool:
    """
    Проверка расширения изображения
    :param image_name: название изображения
    :return: True - формат разрешен / False - формат не разрешен
    """
    with current_app.app_context():
        # Список с разрешенными форматами изображений для загрузки из конфигов
        _allowed_extensions = current_app.config["ALLOWED_EXTENSIONS"]

    # Проверяем, что расширение текущего файла есть в списке разрешенных
    # .rsplit('.', 1) - делит строку, начиная справа; 1 - делит 1 раз (по умолчанию -1 - неограниченное кол-во раз)
    return (
        "." in image_name
        and image_name.rsplit(".", 1)[1].lower() in _allowed_extensions
    )


def clear_path(path: str) -> str:
    """
    Очистка входной строки от "static"
    :param path: строка - полный путь
    :return: очищенная строка
    """
    return path.split("static")[1][1:]


def save_image(image: FileStorage, avatar=False) -> str:
    """
    Сохранение изображения
    :param avatar: переключатель для сохранения аватара пользователя или изображения к твиту
    :param image: файл - изображение
    :return: путь относительно static для сохранения в БД
    """
    with current_app.app_context():
        # Директория для сохранения загружаемых файлов из конфигов
        _upload_folder = current_app.config["UPLOAD"]

    filename = secure_filename(image.filename)  # Проверяем файл для безопасности

    if avatar:
        logger.debug("Сохранение аватара пользователя")
        path = os.path.join(_upload_folder, "avatars", filename)

    else:
        logger.debug("Сохранение изображения к твиту")

        # Сохраняем изображения в директорию по дате добавления твита
        current_date = datetime.now()
        path = os.path.join(
            _upload_folder,
            "tweets",
            f"{current_date.year}",
            f"{current_date.month}",
            f"{current_date.day}",
            filename,
        )

    try:
        logger.info(f"Сохранение картинки в: {path}")

        image.save(path)

    except FileNotFoundError:
        new_path = path.rsplit("/", 1)[0].rsplit("\\", 1)[0]
        logger.warning(f"Создание директории: {new_path}")

        # Создание нескольких вложенных папок
        os.makedirs(new_path)
        image.save(path)

    path = clear_path(path)  # Очищаем строку от "static" для сохранения в БД

    return path


def delete_images(tweet_id: int) -> None:
    """
    Удаление из файловой системы изображений по id твита
    :param tweet_id: id твита
    :return: None
    """
    logger.debug(f"Удаление изображений к твиту №{tweet_id}")

    # Находим изображения по id твита
    images = db.session.execute(
        db.select(Image).filter(Image.tweet_id == tweet_id)
    ).all()

    if images:
        images = list(chain(*images))  # Очищаем результат от вложенных кортежей
        # Директория с изображениями к твиту
        folder = os.path.join(
            "static", images[0].path.rsplit("/", 1)[0].rsplit("\\", 1)[0]
        )

        for img in images:
            try:
                os.remove(
                    os.path.join("static", img.path)
                )  # Удаляем каждое изображение из файловой системы

            except FileNotFoundError:
                logger.error(f"Директория: {img.path} не найдена")

        logger.info("Все изображения удалены")

        check_and_delete_folder(
            path=folder
        )  # Проверка и очистка директории, если пустая

    else:
        logger.warning("Изображения не найдены")


def check_and_delete_folder(path: str) -> None:
    """
    Проверка и удаление папки, если пуста (подчистка пустых директорий после удаления твитов с изображениями)
    :param path: директория с изображениями после удаления твита
    :return: None
    """
    try:
        # Удаляем папку, если пустая
        if len(os.listdir(path)) == 0:
            os.rmdir(path)
            logger.info(f"Директория: {path} удалена")

    except FileNotFoundError:
        logger.error(f"Директория: {path} не найдена")
