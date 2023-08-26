from functools import wraps
from flask import request
from loguru import logger
from http import HTTPStatus

from app.services.user import UserService
from app.schemas.base_response import ErrorResponseSchema


def token_required(func):
    """
    Функция-декоратор для поиска пользователя в БД по api-key из header
    """

    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers.get(
            "api-key", None
        )  # Извлекаем api-key из header запроса

        if token is None:
            logger.error("api_key не передан в header")
            return (
                ErrorResponseSchema().dump(
                    {
                        "error_type": HTTPStatus.UNAUTHORIZED,  # 401 (не авторизован)
                        "error_message": "Valid api-token token is missing",
                    }
                ),
                HTTPStatus.UNAUTHORIZED,
            )

        logger.info(f"api_key: {token}")
        current_user = UserService.get_user_for_key(
            token=token
        )  # Поиск пользователя в БД по api-key

        if current_user is None:
            logger.error("Пользователь не найден")

            return (
                ErrorResponseSchema().dump(
                    {
                        "error_type": HTTPStatus.UNAUTHORIZED,  # 401 (не авторизован)
                        "error_message": "Sorry. Wrong api-key token. This user does not exist",
                    }
                ),
                HTTPStatus.UNAUTHORIZED,
            )

        logger.info(
            f"Пользователь найден: id - {current_user.id}, name - {current_user.name}"
        )

        # Возвращаем объект текущего пользователя из БД
        return func(*args, current_user, **kwargs)

    return decorator
