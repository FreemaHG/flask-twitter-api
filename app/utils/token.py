from functools import wraps
from flask import request
from loguru import logger

from ..services.user import UserService


def token_required(func):
    """
    Функция-декоратор для поиска пользователя в БД по api-key в header
    """

    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers.get('api-key', None)

        if token is None:
            logger.error('api_key не передан в header')

            return {
                'result': False,
                'msg': 'Valid api-token token is missing',
            }, 404

        logger.info(f'api_key: {token}')
        current_user = UserService.get_user_for_key(token)

        if current_user is None:
            logger.error('Пользователь с указанным api-key не найден')

            return {
                'result': False,
                'msg': 'Sorry. Wrong api-key token. This user does not exist.',
            }, 404

        logger.info(f'Пользователь найден: {token}')

        return func(*args, current_user, **kwargs)

    return decorator
