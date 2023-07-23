from typing import Dict

from marshmallow import Schema, fields, validates, post_load, ValidationError

from .base_response import ResponseSchema


class TweetInSchema(Schema):
    """
    Схема для входных данных при добавлении нового твита
    """
    tweet_data = fields.Str(required=True)
    tweet_media_ids = fields.List(fields.Int)

    @validates('tweet_data')
    def validate_tweet_data(self, tweet_data: str) -> None:
        """
        Проверка длины твита
        """
        _limit = 280

        if len(tweet_data) > _limit:
            raise ValidationError(
                f'The length of the tweet should not exceed {_limit} characters. Current value: {len(tweet_data)}'
            )


class TweetResponseSchema(ResponseSchema):
    """
    Схема для вывода id твита после публикации
    """
    tweet_id = fields.Int()


class TweetListSchema(Schema):
    """
    Схема для вывода твитов
    """
    # id = fields.Int()
    # content = fields.Str()
    # attachments = fields.List(fields.Nested(ImageSchema))
    # author = fields.Nested(UserSchema, only=('id', 'name'))
    # likes = fields.List(fields.Nested('LikeSchema', only=('user_id', 'name')))
