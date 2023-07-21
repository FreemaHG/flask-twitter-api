from loguru import logger

from sqlalchemy.orm.exc import NoResultFound

from ..models.users import User
from ..database import db


class UserService:

    @classmethod
    def get_user_for_key(cls, token: str) -> User | None:
        """
        Метод ищет в БД и возвращает объект пользователя по переданному api-key
        :param token: api-ключ пользователя
        :return: объект пользователя / False
        """
        logger.debug(f'Поиск пользователя по api-key: {token}')

        try:
            return db.session.execute(db.select(User).where(User.api_key==token)).scalar_one()

        except NoResultFound:
            logger.error('Пользователь не найден')
            return None

    @classmethod
    def get_user_for_id(cls, user_id: str) -> User | None:
        """
        Метод ищет в БД и возвращает объект пользователя по переданному id
        :param user_id: id пользователя
        :return: объект пользователя / False
        """
        logger.debug(f'Поиск пользователя по id: {user_id}')

        try:
            return db.session.execute(db.select(User).where(User.id==user_id)).scalar_one()

        except NoResultFound:
            logger.error('Пользователь не найден')
            return None
