from marshmallow import ValidationError
from marshmallow import validates
from flasgger import Schema, fields

from app.schemas.base_response import ResponseSchema


class UserSchema(Schema):
    """
    Базовая схема пользователя
    """

    id = fields.Int(dump_only=True)  # dump_only=True - id присваивается после добавления записи в БД
    name = fields.Str(required=True)  # Обязательное поле
    followers = fields.List(fields.Nested("UserSchema", only=("id", "name")))  # Подписчики
    following = fields.List(fields.Nested("UserSchema", only=("id", "name")))  # Подписки

    @validates("name")
    def validate_name(self, name: str) -> None:
        """
        Проверка длины имени пользователя
        """
        _limit = 60

        if len(name) > _limit:
            raise ValidationError(
                f"The username must not exceed {_limit} characters. Current value: {len(name)}"
            )


class UserOutSchema(ResponseSchema):
    """
    Схема для вывода данных о пользователе
    """

    user = fields.Nested(UserSchema)
