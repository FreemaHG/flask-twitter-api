from typing import Dict

from flask import current_app
from marshmallow import Schema, fields, ValidationError, validates_schema
from marshmallow.fields import Field
from werkzeug.datastructures import FileStorage
from loguru import logger

from .base_response import ResponseSchema
from ..utils.media import allowed_image


class ImageSchema(Schema):
    """
    Схема для сохранения изображения к твиту
    """
    file = Field(metadata={'type': 'string', 'format': 'byte'}, allow_none=True, required=True)

    @validates_schema
    def validate_uploaded_file(self, in_data, **kwargs):
        """
        Проверка расширения изображения
        """
        file: FileStorage = in_data.get('file', None)

        logger.debug(f'Файл (название): {file.filename}')
        logger.debug(f'Файл (объект): {file}')

        if file is None:
            raise ValidationError(f'The image is not loaded')

        elif not allowed_image(file.filename):
            allowed_format = ', '.join(elem for elem in current_app.config["ALLOWED_EXTENSIONS"])
            raise ValidationError(f'Invalid images format. Only {allowed_format} files accepted')

        return True


class ImageResponseSchema(ResponseSchema):
    """
    Схема для вывода id изображения после публикации твита
    """
    media_id = fields.Int()


class ImageOutSchema(Schema):
    """
    Схема для вывода ссылки на изображения к твитам
    """
    path = fields.Str()
