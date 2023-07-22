from functools import wraps
from flask import request
from loguru import logger

from ..services.user import UserService
from ..schemas.base_response import ErrorResponseSchema


def token_required(func):
    """
    Функция-декоратор для поиска пользователя в БД по api-key в header
    """

    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers.get('api-key', None)

        if token is None:
            logger.error('api_key не передан в header')
            return ErrorResponseSchema().dump(
                {
                    'error_type': '401',
                    'error_message': 'Valid api-token token is missing'
                }
            ), 401

        logger.info(f'api_key: {token}')
        current_user = UserService.get_user_for_key(token=token)

        if current_user is None:
            return ErrorResponseSchema().dump(
                {
                    'error_type': '401',
                    'error_message': 'Sorry. Wrong api-key token. This user does not exist'
                }
            ), 401

        logger.info(f'Пользователь найден: id - {current_user.id}, name - {current_user.name}')

        return func(*args, current_user, **kwargs)

    return decorator
