from flask_restful import Resource
from loguru import logger

from ..services.user import UserService
from ..schemas.users import UserSchema
from ..utils.token import token_required


class UserData(Resource):

    @token_required
    def get(self, current_user, user_id=None):
        """
        Возврат данных о текущем пользователе
        """

        if user_id is None:
            logger.debug('id пользователя не передан')
            data = UserSchema().dump(current_user)

            return {'result': True, 'user': data}, 200

        user = UserService.get_user_for_id(user_id=user_id)

        if user:
            logger.info('Пользователь найден')
            data = UserSchema().dump(user)

            return {'result': True, 'user': data}, 200

        logger.error(f'Пользователь с id - {user_id} не найден')

        return {
                'result': False,
                'msg': 'Sorry. This user does not exist.',
            }, 404
