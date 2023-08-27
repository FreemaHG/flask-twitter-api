import datetime

from sqlalchemy import func

from app.database import db
from app.models.base import BaseModelMethodsMixin, BaseModelLikeMixin


# Вспомогательная таблица для связи твитов и тегов
tweet_to_tag = db.Table(
    "tweet_to_tag",
    db.Column("tweet_id", db.ForeignKey("tweet.id"), primary_key=True),
    db.Column("tag_id", db.ForeignKey("tag.id"), primary_key=True),
)


class Tweet(db.Model, BaseModelMethodsMixin):
    """
    Модель для хранения твитов
    """

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(280), nullable=False)
    num_likes = db.Column(db.Integer, default=0)
    likes = db.relationship("Like", backref="tweet", cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    images = db.relationship("Image", backref="tweet", cascade="all, delete-orphan")
    tags = db.relationship(
        "Tag",
        secondary=tweet_to_tag,
        backref=db.backref("tweets", lazy="selectin"),
    )


class Image(db.Model, BaseModelMethodsMixin):
    """
    Модель для хранения изображений
    """

    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey("tweet.id"), nullable=True)
    path = db.Column(db.String, nullable=True)


# TODO Не используется!
class Tag(db.Model):
    """
    Модель для хранения тегов
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)


class Like(db.Model, BaseModelMethodsMixin, BaseModelLikeMixin):
    """
    Модель для хранения данных о лайках
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    tweet_id = db.Column(db.Integer, db.ForeignKey("tweet.id"))


# TODO Не используется!
class Comment(db.Model):
    """
    Модель для хранения комментариев к твитам
    """

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(280), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    tweet_id = db.Column(db.Integer, db.ForeignKey("tweet.id"))
    created_at = db.Column(db.String, default=datetime.datetime.now())
