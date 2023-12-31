from itertools import chain
from typing import Dict, List
from sqlalchemy.orm.exc import NoResultFound
from loguru import logger

from app.database import db
from app.models.tweets import Tweet
from app.models.users import User
from app.services.images import ImageService
from app.utils.media import delete_images


class TweetsService:
    """
    Сервис для добавления, удаления и вывода твитов
    """

    @classmethod
    def get_tweets(cls, user: User) -> List[Tweet]:
        """
        Вывод последних твитов подписанных пользователей
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
        Создание нового твита
        :param data: словарь с данными
        :return: объект нового твита
        """
        logger.debug("Сохранение твита в БД")

        # Сохраняем твит
        new_tweet = Tweet(body=data["tweet_data"], user_id=data["user_id"])
        db.session.add(new_tweet)
        db.session.commit()

        # Сохраняем изображения, если есть
        if data["tweet_media_ids"] and data["tweet_media_ids"] != []:
            ImageService.update_images(
                tweet_media_ids=data["tweet_media_ids"], tweet_id=new_tweet.id
            )

        return new_tweet

    @classmethod
    def delete_tweet(cls, user_id: int, tweet_id: int) -> bool | None:
        """
        Удаление твита и его изображений
        :param user_id: id пользователя
        :param tweet_id: id удаляемого твита
        :return: True / False
        """
        logger.debug(f"Удаление твита: id - {tweet_id}")
        logger.debug(f"Пользователь: id - {user_id}")

        tweet = db.session.execute(
            db.select(Tweet).where(Tweet.id == tweet_id)
        ).scalar_one_or_none()

        if tweet:
            logger.debug("Твит найден")
            logger.debug(f"Автор твита: {tweet.user_id}")

            if tweet.user_id == user_id:
                logger.debug("Удаление твита автором")

                delete_images(tweet_id=tweet.id)  # Удаляем изображения твита

                # Удаляем твит
                db.session.delete(tweet)
                db.session.commit()

                return True

            else:
                logger.error("Запрос на удаление чужого твита")
                raise PermissionError("The tweet that is being accessed is locked")

        else:
            logger.error("Твит не найден")
            raise NoResultFound("Tweet not found")
