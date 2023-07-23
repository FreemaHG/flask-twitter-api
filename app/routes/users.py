from flask_restful import Resource
from loguru import logger
from sqlalchemy.exc import NoResultFound

from ..services.user import UserService, FollowerService
from ..schemas.base_response import ErrorResponseSchema, ResponseSchema
from ..schemas.users import UserOutSchema
from ..utils.token import token_required
from ..models.users import User


class UserData(Resource):

    @token_required
    def get(self, current_user: User, user_id=None):
        """
        Возврат данных о пользователе
        """

        if user_id is None:
            logger.warning('id пользователя не передан, возврат данных о текущем пользователе')

            return UserOutSchema().dump({'user': current_user}), 200

        user = UserService.get_user_for_id(user_id=user_id)

        if user:
            logger.info('Пользователь найден')
            return UserOutSchema().dump({'user': user}), 200

        logger.error(f'Пользователь с id - {user_id} не найден')

        return ErrorResponseSchema().dump({'error_message': 'Sorry. This user does not exist'}), 404


class Followers(Resource):

    @token_required
    def post(self, current_user: User, user_id: int):
        """
        Подписка на пользователя
        :param current_user: объект текущего пользователя
        :param user_id: id пользователя для подписки
        """
        try:
            FollowerService.create_follower(current_user=current_user, followed_user_id=user_id)
            return ResponseSchema().dump({'result': True}), 201

        except NoResultFound as exc:
            return ErrorResponseSchema().dump({'error_message': exc}), 404

        except PermissionError as exc:
            return ErrorResponseSchema().dump({'error_type': '423', 'error_message': exc}), 423

    @token_required
    def delete(self, current_user: User, user_id: int):
        """
        Удаление подписки на пользователя
        :param current_user: объект текущего пользователя
        :param user_id: id пользователя для отписки
        """
        try:
            FollowerService.delete_follower(current_user=current_user, followed_user_id=user_id)
            return ResponseSchema().dump({'result': True}), 201

        except NoResultFound as exc:
            return ErrorResponseSchema().dump({'error_message': exc}), 404

        except PermissionError as exc:
            return ErrorResponseSchema().dump({'error_type': '423', 'error_message': exc}), 423
