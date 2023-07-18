from flask_restful import Resource

from flask import request
from loguru import logger

from ..services.user import UserService
from ..schemas.users import UserSchema


class UserData(Resource):

    def get(self):
        """
        Возврат данных о текущем пользователе
        """
        api_key = request.headers.get('api-key')
        logger.info(f'api_key: {api_key}')

        if api_key:
            user = UserService.get_user_for_key(api_key=api_key)

            if user:
                data = UserSchema().dump(user)
                return {'result': True, 'user': data}, 200
            else:
                return 'Нет данных о пользователе', 404

        else:
            logger.error('Не найден api-key в http-header')
            return 'Ошибка в авторизации', 401


class UserDataForId(Resource):

    def get(self, user_id):
        """
        Возврат данных о текущем пользователе
        """
        # user_id = request.args.get('id')
        logger.info(f'user_id: {user_id}')

        if user_id:
            user = UserService.get_user_for_id(user_id=user_id)

            if user:
                data = UserSchema().dump(user)
                return {'result': True, 'user': data}, 200

        return 'Страница не найдена', 404


