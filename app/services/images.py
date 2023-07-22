from typing import Dict, List

from sqlalchemy.exc import NoResultFound
from sqlalchemy import func, select, update
from werkzeug.datastructures import FileStorage
from loguru import logger

from ..database import db
from ..models.tweets import Image
from ..utils.media import save_image


class ImageService:

    @classmethod
    def save_image(cls, images: FileStorage) -> int:
        """
        Метод для сохранения изображения к твиту
        :param images: объект изображения
        :return: id изображения
        """
        path = save_image(image=images)
        image = Image(path=path)

        db.session.add(image)
        db.session.commit()

        return image.id

    @classmethod
    def update_images(cls, tweet_media_ids: List[int], tweet_id: int) -> None:
        """
        Метод для обновления изображений (сохранение ссылки - id твита)
        :param tweet_media_ids: список с id изображений
        :param tweet_id: id твита, к которому принадлежат изображения
        :return: None
        """
        logger.debug(f'Обновление изображений по id: {tweet_media_ids}, tweet_id: {tweet_id}')

        db.session.execute(update(Image).where(Image.id.in_(tweet_media_ids)).values(tweet_id=tweet_id))
        db.session.commit()
