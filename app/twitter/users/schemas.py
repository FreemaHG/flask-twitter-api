from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)  # dump_only=True - id присваивается после добавления записи в БД
    name = fields.Str(required=True)  # Обязательное поле
    followers = fields.List(fields.Nested('UserSchema', only=('id', 'name')))  # Подписчики
    following = fields.List(fields.Nested('UserSchema', only=('id', 'name')))  # Подписки


# class ResponseSchema(Schema):
#     result = fields.Bool(default=True)
#     user = fields.Nested(UserSchema)
#
#
# class ErrorResponseSchema(ResponseSchema):
#     result = fields.Bool(default=False)
#     error_type = fields.Str()
#     error_message = fields.Str()
