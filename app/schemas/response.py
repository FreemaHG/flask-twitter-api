from marshmallow import Schema, fields, validates, post_load, ValidationError

from .users import UserSchema


class ResponseSchema(Schema):
    """
    Базовая схема для ответа
    """
    result = fields.Bool(default=True)


class ErrorResponseSchema(ResponseSchema):
    """
    Схема для ответа с текстом ошибки
    """
    result = fields.Bool(default=False)
    error_type = fields.Str(default='404')
    error_message = fields.Str()


class UserResponseSchema(ResponseSchema):
    """
    Схема для вывода данных о пользователе
    """
    user = fields.Nested(UserSchema)
