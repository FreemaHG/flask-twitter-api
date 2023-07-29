from flask_restful import Resource
from sqlalchemy.exc import NoResultFound
from flasgger import SwaggerView
from http import HTTPStatus
from loguru import logger

from app.services.user import UserService, FollowerService
from app.schemas.base_response import ErrorResponseSchema, ResponseSchema
from app.schemas.users import UserOutSchema
from app.utils.token import token_required
from app.models.users import User


class UserData(Resource):

    @token_required
    def get(self, current_user: User, user_id=None):
        """
        Вывод данных о пользователе
        ---
        tags:
         - users
        parameters:
          - name: api-key
            in: header
            required: true
            type: string
          - name: user_id
            in: path
            required: false
            description: id пользователя для вывода данных
            type: integer
        responses:
          200:
            schema:
              $ref: '#/definitions/UserOut'
          401:
            description: Пользователь не авторизован либо передан некорректный api-key
            schema:
              $ref: '#/definitions/ErrorResponse'
          404:
            description: Пользователь не найден
            schema:
              $ref: '#/definitions/ErrorResponse'
        """

        if user_id is None:
            logger.warning(
                "id пользователя не передан, возврат данных о текущем пользователе"
            )

            return (
                UserOutSchema().dump({"user": current_user}),
                HTTPStatus.OK,
            )  # 200 (успешно)

        user = UserService.get_user_for_id(user_id=user_id)

        if user:
            logger.info("Пользователь найден")
            return UserOutSchema().dump({"user": user}), HTTPStatus.OK  # 200 (успешно)

        logger.error(f"Пользователь с id - {user_id} не найден")

        return (
            ErrorResponseSchema().dump(
                {"error_message": "Sorry. This user does not exist"}
            ),
            HTTPStatus.NOT_FOUND,
        )  # 404 (не найдено)


class Followers(Resource):
    """
    Оформление и удаление подписки на пользователя
    """

    @token_required
    def post(self, current_user: User, user_id: int):
        """
        Подписка на пользователя
        ---
        tags:
          - followers
        parameters:
          - name: api-key
            in: header
            required: true
            type: string
          - name: user_id
            in: path
            required: true
            description: id пользователя для подписки
            type: integer
        responses:
          201:
            description: Подписка оформлена
            schema:
              $ref: '#/definitions/Response'
          401:
            description: Пользователь не авторизован либо передан некорректный api-key
            schema:
              $ref: '#/definitions/ErrorResponse'
          404:
            description: Пользователь не найден
            schema:
              $ref: '#/definitions/ErrorResponse'
          423:
            description: Заблокировано, т.к. пользователь уже подписан
            schema:
              $ref: '#/definitions/ErrorResponse'
        """

        try:
            FollowerService.create_follower(
                current_user=current_user, followed_user_id=user_id
            )
            return ResponseSchema().dump({}), HTTPStatus.CREATED  # 201 (создано)

        except NoResultFound as exc:
            return (
                ErrorResponseSchema().dump({"error_message": exc}),
                HTTPStatus.NOT_FOUND,
            )  # 404 (не найдено)

        except PermissionError as exc:
            return (
                ErrorResponseSchema().dump(
                    {"error_type": HTTPStatus.LOCKED, "error_message": exc}
                ),
                HTTPStatus.LOCKED,
            )  # 423 (заблокировано)

    @token_required
    def delete(self, current_user: User, user_id: int):
        """
        Удаление подписки
        ---
        tags:
          - followers
        parameters:
          - name: api-key
            in: header
            required: true
            type: string
          - name: user_id
            in: path
            required: true
            description: id пользователя для удаления подписки
            type: integer
        responses:
          200:
            description: Подписка удалена
            schema:
              $ref: '#/definitions/Response'
          401:
            description: Пользователь не авторизован либо передан некорректный api-key
            schema:
              $ref: '#/definitions/ErrorResponse'
          404:
            description: Пользователь не найден
            schema:
              $ref: '#/definitions/ErrorResponse'
          423:
            description: Заблокировано, т.к. пользователь еще не подписан
            schema:
              $ref: '#/definitions/ErrorResponse'
        """

        try:
            FollowerService.delete_follower(
                current_user=current_user, followed_user_id=user_id
            )
            return ResponseSchema().dump({}), HTTPStatus.OK  # 200

        except NoResultFound as exc:
            return (
                ErrorResponseSchema().dump({"error_message": exc}),
                HTTPStatus.NOT_FOUND,
            )  # 404 (не найдено)

        except PermissionError as exc:
            return (
                ErrorResponseSchema().dump(
                    {"error_type": HTTPStatus.LOCKED, "error_message": exc}
                ),
                HTTPStatus.LOCKED,
            )  # 423 (заблокировано)
