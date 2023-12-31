from loguru import logger

from sqlalchemy.orm.exc import NoResultFound

from app.models.users import User
from app.database import db


class UserService:
    """
    Сервис для вывода данных о пользователе
    """

    @classmethod
    def get_user_for_key(cls, token: str) -> User | None:
        """
        Возврат объекта пользователя по api-key
        :param token: api-ключ пользователя
        :return: объект пользователя / False
        """
        logger.debug(f"Поиск пользователя по api-key: {token}")

        return db.session.execute(
            db.select(User).where(User.api_key == token)
        ).scalar_one_or_none()

    @classmethod
    def get_user_for_id(cls, user_id: int) -> User | None:
        """
        Возврат объекта пользователя по id
        :param user_id: id пользователя
        :return: объект пользователя / False
        """
        logger.debug(f"Поиск пользователя по id: {user_id}")

        return db.session.execute(
            db.select(User).where(User.id == user_id)
        ).scalar_one_or_none()


class FollowerService:
    """
    Сервис для оформления, удаления и проверки подписок пользователей друг на друга
    """

    @classmethod
    def create_follower(cls, current_user: User, followed_user_id: int) -> None:
        """
        Создание подписки на пользователя по id
        :param current_user: объект текущего пользователя
        :param followed_user_id: id пользователя для подписки
        :return: None
        """
        followed_user = UserService.get_user_for_id(user_id=followed_user_id)

        if followed_user:
            if cls.check_follower(
                current_user=current_user, followed_user=followed_user
            ):
                logger.error("Пользователь уже подписан")
                raise PermissionError("The subscription has already been issued")

            else:
                logger.debug("Оформление новой подписки")
                current_user.following.append(followed_user)
                db.session.commit()
        else:
            logger.error("Пользователь для подписки не найден")
            raise NoResultFound("The subscription user was not found")

    @classmethod
    def check_follower(cls, current_user: User, followed_user: User) -> bool:
        """
        Проверка подписки
        :param current_user: объект текущего пользователя
        :param followed_user: объект пользователя для подписки
        :return: True - подписка / False - нет подписки
        """
        logger.debug("Проверка подписки")

        if current_user is followed_user:
            logger.error("Попытка подписки на самого себя")
            raise PermissionError("You can not subscribe to yourself")

        return followed_user in current_user.following

    @classmethod
    def delete_follower(cls, current_user: User, followed_user_id: int) -> None:
        """
        Отмена подписки на пользователя по id
        :param current_user: объект текущего пользователя
        :param followed_user_id: id пользователя для отписки
        :return: None
        """
        followed_user = UserService.get_user_for_id(user_id=followed_user_id)

        if followed_user:
            if not cls.check_follower(
                current_user=current_user, followed_user=followed_user
            ):
                logger.error("Пользователь нет в числе подписчиков")
                raise PermissionError("The user is not among the subscribers")

            else:
                logger.debug("Отмена подписки")
                current_user.following.remove(followed_user)
                db.session.commit()
        else:
            logger.error("Пользователь для отмены подписки не найден")
            raise NoResultFound("The user to cancel the subscription was not found")
