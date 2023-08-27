from sqlalchemy import event, func

from app.database import db
from app.models.tweets import Tweet, Like
from app.models.base import BaseModelMethodsMixin, BaseModelUserMixin


# Вспомогательная таблица для отслеживания подписок пользователей между собой
user_to_user = db.Table(
    "followers",
    db.Column("user_id", db.ForeignKey("user.id"), primary_key=True),
    db.Column("following_user_id", db.ForeignKey("user.id"), primary_key=True),
)


class User(db.Model, BaseModelMethodsMixin, BaseModelUserMixin):
    """
    Модель для хранения данных о пользователях
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    api_key = db.Column(db.String(60))
    password = db.Column(db.String)
    avatar = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=func.now())
    tweets = db.relationship(Tweet, backref="user", cascade="all, delete-orphan")
    likes = db.relationship(Like, backref="user", cascade="all, delete-orphan")

    # Многие ко многим (подписки пользователей друг на друга)
    following = db.relationship(
        "User",
        secondary=user_to_user,
        backref=db.backref("followers", lazy="selectin"),
        primaryjoin=id == user_to_user.c.user_id,
        secondaryjoin=id == user_to_user.c.following_user_id,
    )


# FIXME Удалить или использовать...
@event.listens_for(User, "after_delete")
def event_after_delete(mapper, connection, target):
    # Здесь будет очень важная бизнес логика
    # Или нет. На самом деле, старайтесь использовать сигналы только
    # тогда, когда других, более правильных вариантов не осталось.
    pass
