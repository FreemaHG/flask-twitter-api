from loguru import logger
from sqlalchemy.orm import Session

from ..models.tweets import Tweet, Like
from ..database import db


class LikesService:

    @classmethod
    def get_tweet(cls, tweet_id: int) -> Tweet | None:
        """
        Метод для получения твита по переданному id
        :param tweet_id: id твита
        :return: объект твита / None
        """
        logger.debug(f'Поиск твита по id - {tweet_id}')

        return db.session.execute(db.select(Tweet).where(Tweet.id == tweet_id)).scalar_one_or_none()

    @classmethod
    def check_like_tweet(cls, tweet_id: int, user_id: int):
        """
        Проверка, что данный пользователь еще не ставил лайк твиту
        :param tweet_id: id твита
        :param user_id: id пользователя
        """
        return db.session.execute(
            db.select(Like).where(Like.user_id == user_id, Like.tweet_id == tweet_id)).scalar_one_or_none()

    @classmethod
    def like_tweet(cls, tweet: Tweet, user_id: int) -> None:
        """
        Метод отмечает лайк для переданного твита, изменяет кол-во лайков
        :param tweet: объект твита
        :param user_id: id пользователя
        :return: None
        """

        if not cls.check_like_tweet(tweet_id=tweet.id, user_id=user_id):
            tweet.num_likes += 1
            like_record = Like(user_id=user_id, tweet_id=tweet.id)
            db.session.add(like_record)
            db.session.commit()

        else:
            logger.error('Пользователь уже ставил лайк данному твиту')
            raise PermissionError('The user has already liked this tweet')

    @classmethod
    def delete_like(cls, tweet: Tweet, user_id: int) -> None:
        """
        Удаление лайка с твита
        :param tweet: объект твита
        :param user_id: id пользователя
        :return: None
        """
        if cls.check_like_tweet(tweet_id=tweet.id, user_id=user_id):
            like_record = db.session.execute(
                db.select(Like).where(Like.user_id == user_id, Like.tweet_id == tweet.id)).scalar_one_or_none()

            if like_record:
                db.session.delete(like_record)
            else:
                logger.error('Запись о лайке не найдена')

            tweet.num_likes -= 1

            if tweet.num_likes < 0:
                tweet.num_likes = 0

            db.session.commit()

        else:
            logger.error('Пользователь еще не ставил лайк данному твиту')
            raise PermissionError('The user has not yet liked this tweet')
