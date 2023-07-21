from marshmallow import Schema, fields, validates, post_load, ValidationError

# from flasgger import Schema, fields, ValidationError


class UserSchema(Schema):
    id = fields.Int(dump_only=True)  # dump_only=True - id присваивается после добавления записи в БД
    name = fields.Str(required=True)  # Обязательное поле
    followers = fields.List(fields.Nested('UserSchema', only=('id', 'name')))  # Подписчики
    following = fields.List(fields.Nested('UserSchema', only=('id', 'name')))  # Подписки

    @validates('name')
    def validate_name(self, name: str) -> None:
        """
        Валидация имени: проверка, чтобы
        :param name:
        :return:
        """
        _limit = 60

        if len(name) > _limit:
            raise ValidationError(f'Имя пользователя не должно превышать {_limit} символов')
