from marshmallow import Schema, fields

from .users import UserSchema


class LikeSchema(Schema):
    """
    Схема для вывода лайков при выводе твитов
    """
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    user = fields.Pluck(UserSchema, 'name', data_key='name')
