from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound
from http import HTTPStatus
from loguru import logger

from app.utils.token import token_required
from app.services.tweets import TweetsService
from app.models.users import User
from app.schemas.tweets import TweetResponseSchema, TweetInSchema, TweetListSchema
from app.schemas.base_response import ErrorResponseSchema, ResponseSchema


class TweetsList(Resource):

    @token_required
    def get(self, current_user: User):
        """
        Вывод твитов
        ---
        tags:
          - tweets
        description: Выводятся последние твиты подписчиков
        parameters:
          - name: api-key
            in: header
            required: true
            type: string
        responses:
          200:
            schema:
              $ref: '#/definitions/TweetList'
          401:
            description: Пользователь не авторизован либо передан некорректный api-key
            schema:
              $ref: '#/definitions/ErrorResponse'
        """

        logger.debug(f"Вывод твитов")
        tweets = TweetsService.get_tweets(user=current_user)

        return (
            TweetListSchema().dump({"tweets": tweets}),
            HTTPStatus.OK,
        )  # 200 (успешно)

    @token_required
    def post(self, current_user: User):
        """
        Добавление твита
        ---
        tags:
          - tweets
        description: Публикация твита (изображения не обязательны). При передаче изображений в форму автоматически вызывается ендпоинт для их сохранения
        parameters:
          - name: api-key
            in: header
            required: true
            type: string
          - name: body
            in: body
            required: true
            description: Добавление твита
            schema:
              $ref: '#/definitions/TweetIn'
        responses:
          201:
            description: Твит добавлен
            schema:
              $ref: '#/definitions/TweetResponse'
          401:
            description: Пользователь не авторизован либо передан некорректный api-key
            schema:
              $ref: '#/definitions/ErrorResponse'
          400:
            description: Невалидные данные
            schema:
              $ref: '#/definitions/ErrorResponse'
        """

        logger.debug("Добавление твита")

        data = request.json
        data["user_id"] = current_user.id

        try:
            TweetInSchema().load(
                {"tweet_data": data["tweet_data"]}
            )  # Валидация входных данных
            tweet = TweetsService.create_tweet(data=data)

            return (
                TweetResponseSchema().dump({"tweet_id": tweet.id}),
                HTTPStatus.CREATED,
            )  # 201 (создано)

        except ValidationError as exc:
            logger.error(f"Невалидные данные: {exc.messages}")
            error_message = exc.messages["tweet_data"][0]

            return (
                ErrorResponseSchema().dump(
                    {
                        "error_type": HTTPStatus.BAD_REQUEST,
                        "error_message": error_message,
                    }
                ),
                HTTPStatus.BAD_REQUEST,
            )  # 400 (невалидные данные)


class TweetItem(Resource):

    @token_required
    def delete(self, current_user: User, tweet_id: int):
        """
        Удаление твита
        ---
        tags:
          - tweets
        description: Пользователь может удалять только свои твиты
        parameters:
          - name: api-key
            in: header
            required: true
            type: string
          - name: tweet_id
            in: path
            required: true
            description: id твита для удаления
            type: integer
        responses:
          200:
            description: Твит удален
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
            description: Заблокировано, нельзя удалить чужой твит
            schema:
              $ref: '#/definitions/ErrorResponse'
        """

        logger.debug("Удаление твита")

        try:
            TweetsService.delete_tweet(user_id=current_user.id, tweet_id=tweet_id)
            return ResponseSchema().dump({}), HTTPStatus.OK  # 200 (успешно)

        except PermissionError as exc:
            return (
                ErrorResponseSchema().dump({"error_type": f"{HTTPStatus.LOCKED}", "error_message": exc}),
                HTTPStatus.LOCKED,
            )  # 423 (заблокировано)

        except NoResultFound as exc:
            return (
                ErrorResponseSchema().dump({"error_message": exc}),
                HTTPStatus.NOT_FOUND,
            )  # 404 (не найдено)
