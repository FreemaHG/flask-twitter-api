from marshmallow import Schema
from marshmallow import Schema, fields, validate, ValidationError, post_load


class BaseSchema(Schema):
    result = fields.Bool(default=True)


from typing import Dict
from marshmallow import Schema, fields, validate, ValidationError, post_load


# TODO В работе...
# class UserSchema(Schema):
#     id = fields.Int(dump_only=True)
#     name = fields.Str(required=True)
#     followers = fields.List(UserSchema)  # Подписчики
#     following = fields.List(UserSchema)  # На кого подписан


