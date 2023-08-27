from app.database import db


class BaseModelMethodsMixin:
    """
    Базовый клас для сохранения и удаления записи из БД
    """
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()


class BaseModelUserMixin:

    def get_by_token(self, token):
        return db.session.execute(db.select('User').where('User.api_key' == token)).scalar_one_or_none()


class BaseModelLikeMixin:

    def get_by_ids(self, like_id):
        return db.session.execute(db.select('Like').where('Like.id' == like_id)).scalar_one_or_none()

