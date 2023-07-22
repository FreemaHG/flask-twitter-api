import datetime

from ..database import db


# Вспомогательная таблица для связи твитов и тегов
tags = db.Table(
    'tags',
    db.Column('tweet_id', db.ForeignKey('tweet.id'), primary_key=True),
    db.Column('tag_id', db.ForeignKey('tag.id'), primary_key=True)
)


class Tweet(db.Model):
    """
    Модель для хранения твитов
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(280), nullable=False)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.String, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    images = db.relationship('Image', backref='tweet', cascade='all, delete-orphan')
    tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('tweets', lazy='selectin'),
        primaryjoin=id == tags.c.tweet_id,
        secondaryjoin=id == tags.c.tag_id,
    )


class Image(db.Model):
    """
    Модель для хранения данных об изображениях для твитов
    """
    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'), nullable=True)
    path = db.Column(db.String, nullable=True)


class Tag(db.Model):
    """
    Модель для хранения тегов для твитов
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)


class Like(db.Model):
    """
    Модель для хранения данных о лайках
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'))


class Comment(db.Model):
    """
    Модель для хранения комментариев к твитам
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(280), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'))
    created_at = db.Column(db.String, default=datetime.datetime.now())
