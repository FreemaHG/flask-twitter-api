from flask_restful import Resource
from loguru import logger

from ..services.user import UserService
from ..schemas.response import UserResponseSchema, ErrorResponseSchema
from ..utils.token import token_required


class UserData(Resource):

    @token_required
    def get(self, current_user, user_id=None):
        """
        Возврат данных о пользователе
        """

        if user_id is None:
            logger.warning('id пользователя не передан, возврат данных о текущем пользователе')

            return UserResponseSchema().dump({'user': current_user}), 200

        user = UserService.get_user_for_id(user_id=user_id)

        if user:
            logger.info('Пользователь найден')
            return UserResponseSchema().dump({'user': user}), 200

        logger.error(f'Пользователь с id - {user_id} не найден')

        return ErrorResponseSchema().dump({'error_message': 'Sorry. This user does not exist'}), 404