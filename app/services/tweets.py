from itertools import chain
from typing import Dict, List
from sqlalchemy.orm.exc import NoResultFound
from loguru import logger

from ..database import db
from ..models.tweets import Tweet
from ..models.users import User
from ..services.images import ImageService
from ..utils.media import delete_image


class TweetsService:

    @classmethod
    def get_tweets(cls, user: User) -> List[Tweet]:
        """
        Метод для вывода последних твитов у подписанных пользователей
        :param user: объект текущего пользователя
        :return: список с твитами
        """

        tweets = db.session.execute(
            db.select(Tweet)
            .filter(Tweet.user_id.in_(user.id for user in user.following))
            .order_by(Tweet.created_at.desc())
        ).all()

        # Очистка результатов от вложенных кортежей
        tweets = list(chain(*tweets))

        return tweets

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

    @classmethod
    def delete_tweet(cls, user_id: int, tweet_id: int) -> bool | None:
        """
        Метод для удаления твита с его изображениями
        :param user_id: id пользователя
        :param tweet_id: id удаляемого твита
        :return: True / False
        """
        logger.debug(f'Удаление твита: id - {tweet_id}')
        tweet = db.session.execute(db.select(Tweet).where(Tweet.id == tweet_id)).scalar_one_or_none()

        if tweet:
            logger.debug('Твит найден')

            if tweet.user_id == user_id:
                logger.debug('Удаление твита автором')

                delete_image(tweet_id=tweet.id)  # Удаляем изображения твита

                db.session.delete(tweet)
                db.session.commit()

                return True

            else:
                logger.error('Запрос на удаление чужого твита')
                raise PermissionError('The tweet that is being accessed is locked')

        else:
            logger.error('Твит не найден')
            raise NoResultFound('Tweet not found')
