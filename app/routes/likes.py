from flask_restful import Resource
from http import HTTPStatus
from loguru import logger

from app.utils.token import token_required
from app.models.users import User
from app.services.likes import LikesService
from app.schemas.base_response import ErrorResponseSchema, ResponseSchema


class LikesRoute(Resource):
    _not_found_message = "Tweet not found"

    @token_required
    def post(self, current_user: User, tweet_id: int):
        """
        Добавление лайка к твиту
        ---
        tags:
          - likes
        # Защищаем метод (ендпоинт) авторизацией через токен в header (см. __init__.py, create_swagger - APIKeyHeader)
        security:
         - APIKeyHeader: []
        parameters:
          - name: tweet_id
            in: path
            required: true
            description: id твита для лайка
            type: integer
        responses:
          201:
            description: Лайк поставлен
            schema:
              $ref: '#/definitions/Response'
          401:
            description: Пользователь не авторизован либо передан некорректный api-key
            schema:
              $ref: '#/definitions/ErrorResponse'
          404:
            description: Твит не найден
            schema:
              $ref: '#/definitions/ErrorResponse'
          423:
            description: Заблокировано, т.к. пользователь уже ставил лайк твиту
            schema:
              $ref: '#/definitions/ErrorResponse'
        """

        tweet = LikesService.get_tweet(tweet_id=tweet_id)

        if tweet:
            try:
                LikesService.like_tweet(tweet=tweet, user_id=current_user.id)
                return ResponseSchema().dump({}), HTTPStatus.CREATED  # 201 (создано)

            except PermissionError as exc:
                return (
                    ErrorResponseSchema().dump(
                        {"error_type": HTTPStatus.LOCKED, "error_message": exc}
                    ),
                    HTTPStatus.LOCKED,
                )  # 423 (заблокировано)

        logger.error("Твит не найден")

        return (
            ErrorResponseSchema().dump({"error_message": self._not_found_message}),
            HTTPStatus.NOT_FOUND,
        )  # 404

    @token_required
    def delete(self, current_user: User, tweet_id: int):
        """
        Удаление лайка
        ---
        tags:
          - likes
        security:
         - APIKeyHeader: []
        parameters:
          - name: tweet_id
            in: path
            required: true
            description: ID твита для удаления лайка
            type: integer
        responses:
          200:
            description: Лайк удален
            schema:
              $ref: '#/definitions/Response'
          401:
            description: Пользователь не авторизован либо передан некорректный api-key
            schema:
              $ref: '#/definitions/ErrorResponse'
          404:
            description: Твит не найден
            schema:
              $ref: '#/definitions/ErrorResponse'
          423:
            description: Заблокировано, т.к. пользователь еще не ставил лайк твиту
            schema:
              $ref: '#/definitions/ErrorResponse'
        """

        tweet = LikesService.get_tweet(tweet_id=tweet_id)

        if tweet:
            try:
                LikesService.delete_like(tweet=tweet, user_id=current_user.id)
                return ResponseSchema().dump({}), HTTPStatus.OK  # 200

            except PermissionError as exc:
                return (
                    ErrorResponseSchema().dump(
                        {"error_type": HTTPStatus.LOCKED, "error_message": exc}
                    ),
                    HTTPStatus.LOCKED,
                )  # 423 (заблокировано)

        logger.error("Твит не найден")

        return (
            ErrorResponseSchema().dump({"error_message": self._not_found_message}),
            HTTPStatus.NOT_FOUND,
        )  # 404
