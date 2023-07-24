from flask_restful import Resource
from loguru import logger

from ..utils.token import token_required
from ..models.users import User
from ..services.likes import LikesService
from ..schemas.base_response import ErrorResponseSchema, ResponseSchema


class LikesRoute(Resource):

    _not_found_message = 'Tweet not found'

    @token_required
    def post(self, current_user: User, tweet_id: int):
        """
        Добавление лайка к твиту
        :param current_user: текущий пользователь
        :param tweet_id: id твита
        """
        tweet = LikesService.get_tweet(tweet_id=tweet_id)

        if tweet:
            try:
                LikesService.like_tweet(tweet=tweet, user_id=current_user.id)
                return ResponseSchema().dump({}), 201

            except PermissionError as exc:
                return ErrorResponseSchema().dump({'error_type': '423', 'error_message': exc}), 423

        logger.error('Твит не найден')

        return ErrorResponseSchema().dump({'error_message': self._not_found_message}), 404

    @token_required
    def delete(self, current_user: User, tweet_id: int):
        """
        Удаление лайка с твита
        :param current_user: текущий пользователь
        :param tweet_id: id твита
        """
        tweet = LikesService.get_tweet(tweet_id=tweet_id)

        if tweet:
            try:
                LikesService.delete_like(tweet=tweet, user_id=current_user.id)
                return ResponseSchema().dump({}), 201

            except PermissionError as exc:
                return ErrorResponseSchema().dump({'error_type': '423', 'error_message': exc}), 423

        logger.error('Твит не найден')

        return ErrorResponseSchema().dump({'error_message': self._not_found_message}), 404
