from marshmallow import validates, ValidationError
from flasgger import Schema, fields

from app.schemas.base_response import ResponseSchema
from app.schemas.images import ImageOutSchema
from app.schemas.users import UserSchema
from app.schemas.likes import LikeSchema


class TweetInSchema(Schema):
    """
    Схема для входных данных при добавлении нового твита
    """

    tweet_data = fields.Str(required=True)
    tweet_media_ids = fields.List(fields.Int)

    @validates("tweet_data")
    def validate_tweet_data(self, tweet_data: str) -> None:
        """
        Проверка длины твита
        """
        _limit = 280

        if len(tweet_data) > _limit:
            raise ValidationError(
                f"The length of the tweet should not exceed {_limit} characters. Current value: {len(tweet_data)}"
            )


class TweetResponseSchema(ResponseSchema):
    """
    Схема для вывода id твита после публикации
    """

    tweet_id = fields.Int()


class TweetOutSchema(Schema):
    """
    Схема для вывода твита, автора, вложенных изображений и данных по лайкам
    """

    id = fields.Int()
    body = fields.Str(data_key="content")
    images = fields.Pluck(ImageOutSchema, "path", many=True, data_key="attachments")
    user = fields.Nested(UserSchema, only=("id", "name"), data_key="author")
    likes = fields.List(fields.Nested(LikeSchema, only=("user_id", "user.name")))


class TweetListSchema(ResponseSchema):
    """
    Схема для вывода списка твитов
    """

    tweets = fields.List(fields.Nested(TweetOutSchema))
