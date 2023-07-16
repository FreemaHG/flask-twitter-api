from flask_restful import Resource

from flask import request
from loguru import logger

from .services.user import UserService


class UserData(Resource):

    def get(self):
        """
        Возврат данных о текущем пользователе
        """
        logger.debug('Отработка GET-метода')

        api_key = request.headers.get('api-key')
        logger.info(f'api_key: {api_key}')

        if api_key:
            res = UserService.get_user(api_key=api_key)

            if res:
                return {'data': res}, 200
            else:
                return 'Нет данных о пользователей', 404

        else:
            logger.error('Не найден api-key в http-header')
            return 'Ошибка в авторизации', 401
