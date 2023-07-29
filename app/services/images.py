from typing import List

from sqlalchemy import update
from werkzeug.datastructures import FileStorage
from loguru import logger

from app.database import db
from app.models.tweets import Image
from app.utils.media import save_image


class ImageService:
    """
    Сервис для сохранения изображений при добавлении нового твита
    """

    @classmethod
    def save_image(cls, images: FileStorage) -> int:
        """
        Сохранение изображения (без привязки к твиту)
        :param images: файл
        :return: id изображения
        """
        logger.debug("Сохранение изображения")

        path = save_image(image=images)  # Сохранение изображения в файловой системе
        image = Image(path=path)  # Создание экземпляра изображения
        db.session.add(image)  # Добавление изображения в БД
        db.session.commit()  # Сохранение в БД

        return image.id

    @classmethod
    def update_images(cls, tweet_media_ids: List[int], tweet_id: int) -> None:
        """
        Обновление изображений (привязка к твиту)
        :param tweet_media_ids: список с id изображений
        :param tweet_id: id твита для привязки изображений
        :return: None
        """
        logger.debug(
            f"Обновление изображений по id: {tweet_media_ids}, tweet_id: {tweet_id}"
        )

        db.session.execute(
            update(Image).where(Image.id.in_(tweet_media_ids)).values(tweet_id=tweet_id)
        )
        db.session.commit()
