from flask import current_app
from marshmallow import ValidationError, validates_schema
from marshmallow.fields import Field
from flasgger import Schema, fields
from werkzeug.datastructures import FileStorage

from app.schemas.base_response import ResponseSchema
from app.utils.media import allowed_image


class ImageInSchema(Schema):
    """
    Схема для добавления изображения к твиту
    """

    file = Field(
        metadata={"type": "string", "format": "byte"}, allow_none=True, required=True
    )

    @validates_schema
    def validate_uploaded_file(self, in_data, **kwargs):
        """
        Проверка расширения загружаемого изображения
        """
        file: FileStorage = in_data.get("file", None)

        if file is None:
            raise ValidationError(f"The image is not loaded")

        elif not allowed_image(file.filename):
            allowed_format = ", ".join(
                elem for elem in current_app.config["ALLOWED_EXTENSIONS"]
            )
            raise ValidationError(
                f"Invalid images format. Only {allowed_format} files accepted"
            )

        return True


class ImageResponseSchema(ResponseSchema):
    """
    Схема для вывода id изображения после публикации твита
    """

    media_id = fields.Int()


class ImageOutSchema(Schema):
    """
    Схема для вывода ссылки на изображения при отображении твитов
    """

    path = fields.Str()
