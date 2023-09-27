from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from http import HTTPStatus
from loguru import logger

from app.schemas.base_response import ErrorResponseSchema
from app.utils.token import token_required
from app.services.images import ImageService
from app.models.users import User
from app.schemas.images import ImageInSchema, ImageResponseSchema


class AddImages(Resource):
    @token_required
    def post(self, current_user: User):
        """
        Загрузка изображения к твиту
        ---
        tags:
          - images
        # Защищаем метод (ендпоинт) авторизацией через токен в header (см. __init__.py, create_swagger - APIKeyHeader)
        security:
         - APIKeyHeader: []
        description: Ендпоинт вызывается автоматически для каждого погружаемого изображения при публикации твита с последующей привязкой к твиту
        parameters:
          - name: file
            in: formData
            description: Изображение для загрузки
            required: false
            type: file
        responses:
          201:
            description: Успешная загрузка изображения
            schema:
              $ref: '#/definitions/ImageResponse'
          401:
            description: Пользователь не авторизован либо передан некорректный api-key
            schema:
              $ref: '#/definitions/ErrorResponse'
          422:
            description: Неразрешенный формат изображения
            schema:
              $ref: '#/definitions/ErrorResponse'
        """

        logger.debug("Загрузка изображения к твиту")

        images = request.files["file"]
        logger.info(f"Файл: {images}")

        try:
            ImageInSchema().load({"file": images})
            media_id = ImageService.save_image(images=images)

            return (
                ImageResponseSchema().dump({"media_id": media_id}),
                HTTPStatus.CREATED,
            )  # 201 (создан)

        except ValidationError as exc:
            logger.error(f"Невалидные данные: {exc.messages}")
            error_message = exc.messages["_schema"][0]

            return (
                ErrorResponseSchema().dump(
                    {
                        "error_type": HTTPStatus.UNPROCESSABLE_ENTITY,  # 422 (изображения неразрешенного формата)
                        "error_message": error_message,
                    }
                ),
                HTTPStatus.UNPROCESSABLE_ENTITY,
            )
