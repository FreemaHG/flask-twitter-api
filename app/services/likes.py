from loguru import logger

from app.models.tweets import Tweet, Like
from app.database import db


class LikesService:
    """
    Сервис для добавления, удаления и проверки лайков
    """

    @classmethod
    def get_tweet(cls, tweet_id: int) -> Tweet | None:
        """
        Возврат твита по id
        :param tweet_id: id твита
        :return: объект твита / None
        """
        logger.debug(f"Поиск твита по id - {tweet_id}")

        return db.session.execute(
            db.select(Tweet).where(Tweet.id == tweet_id)
        ).scalar_one_or_none()

    @classmethod
    def check_like_tweet(cls, tweet_id: int, user_id: int) -> Like | None:
        """
        Проверка лайка (метод возвращает запись о лайке, проверяя тем самым, ставил ли пользователь лайк
        указанному твиту)
        :param tweet_id: id твита
        :param user_id: id пользователя
        """

        return db.session.execute(
            db.select(Like).where(Like.user_id == user_id, Like.tweet_id == tweet_id)
        ).scalar_one_or_none()

    @classmethod
    def like_tweet(cls, tweet: Tweet, user_id: int) -> None:
        """
        Сохранение лайка твиту с изменением счетчика лайков твита
        :param tweet: объект твита
        :param user_id: id пользователя
        :return: None
        """

        if not cls.check_like_tweet(tweet_id=tweet.id, user_id=user_id):
            tweet.num_likes += 1  # Увеличиваем счетчик с лайками
            like_record = Like(
                user_id=user_id, tweet_id=tweet.id
            )  # Создаем запись о лайке
            db.session.add(like_record)
            db.session.commit()

        else:
            logger.error("Пользователь уже ставил лайк данному твиту")
            raise PermissionError("The user has already liked this tweet")

    @classmethod
    def delete_like(cls, tweet: Tweet, user_id: int) -> None:
        """
        Удаление лайка
        :param tweet: объект твита
        :param user_id: id пользователя
        :return: None
        """
        if cls.check_like_tweet(tweet_id=tweet.id, user_id=user_id):
            like_record = db.session.execute(
                db.select(Like).where(
                    Like.user_id == user_id, Like.tweet_id == tweet.id
                )
            ).scalar_one_or_none()

            if not like_record:
                logger.error("Запись о лайке не найдена")

            else:
                db.session.delete(like_record)  # Удаляем лайк
                tweet.num_likes -= 1  # Уменьшаем счетчик лайков твита

                # Проверка, чтобы лайки не уходили в минус
                if tweet.num_likes < 0:
                    tweet.num_likes = 0

                db.session.commit()

        else:
            logger.error("Пользователь еще не ставил лайк данному твиту")
            raise PermissionError("The user has not yet liked this tweet")
