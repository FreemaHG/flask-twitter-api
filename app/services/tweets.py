from typing import Dict, List
from loguru import logger

from ..database import db
from ..models.tweets import Tweet, Image, Like, Comment
from ..services.images import ImageService


class TweetsService:

    @classmethod
    def create_tweet(cls, data: Dict) -> Tweet:
        """
        Метод для сохранения нового твита
        :param data: словарь с данными
        :return: объект нового твита
        """
        logger.debug('Сохранение твита в БД')

        new_tweet = Tweet(
            body=data['tweet_data'],
            user_id=data['user_id'],
        )

        db.session.add(new_tweet)
        db.session.commit()

        if data['tweet_media_ids']:
            ImageService.update_images(tweet_media_ids=data['tweet_media_ids'], tweet_id=new_tweet.id)

        return new_tweet
