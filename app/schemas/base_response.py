from flasgger import Schema, fields
from http import HTTPStatus


class ResponseSchema(Schema):
    """
    Базовая схема для успешного ответа
    """

    result = fields.Bool(dump_default=True)


class ErrorResponseSchema(ResponseSchema):
    """
    Схема для неуспешного ответа с типом и текстом ошибки
    """

    result = fields.Bool(dump_default=False)
    error_type = fields.Str(dump_default=HTTPStatus.NOT_FOUND)
    error_message = fields.Str()
