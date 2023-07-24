from marshmallow import Schema, fields


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
    error_type = fields.Str(dump_default='404')
    error_message = fields.Str()
