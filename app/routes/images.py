from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from loguru import logger

from ..schemas.base_response import ErrorResponseSchema
from ..utils.token import token_required
from ..services.images import ImageService
from ..models.users import User
from ..schemas.images import ImageInSchema, ImageResponseSchema


class AddImages(Resource):

    @token_required
    def post(self, current_user: User):
        """
        Загрузка изображения к твиту
        """
        logger.debug('Загрузка изображения к твиту')

        images = request.files['file']
        logger.info(f'Файл: {images}')

        try:
            ImageInSchema().load({'file': images})
            media_id = ImageService.save_image(images=images)

            return ImageResponseSchema().dump({'media_id': media_id}), 201

        except ValidationError as exc:
            logger.error(f'Невалидные данные: {exc.messages}')
            error_message = exc.messages['_schema'][0]

            return ErrorResponseSchema().dump({'error_type': 422, 'error_message': error_message}), 422
