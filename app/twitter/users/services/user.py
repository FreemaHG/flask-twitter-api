from loguru import logger

from ..models import User
from ...database import db


class UserService:

    @classmethod
    def get_user(cls, api_key: str) -> User | None:
        """
        Метод ищет в БД и возвращает объект пользователя по переданному api-key
        :param key: api-ключ пользователя
        :return: объект пользователя / False
        """
        logger.debug(f'Поиск пользователя по api-key: {api_key}')

        # FIXME Оптимизировать в одну строку после отладки
        user = db.session.execute(db.select(User).where(User.api_key==api_key)).scalar_one()
        logger.debug(f'Результат поиска: username - {user.name}, api-key: {user.api_key}')

        return user
