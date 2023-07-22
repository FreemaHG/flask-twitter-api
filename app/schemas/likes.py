from marshmallow import Schema, fields, validates, post_load, ValidationError


class LikeSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    name = fields.Str()
