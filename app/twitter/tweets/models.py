import datetime

from ..database import db


class Tweet(db.Model):
    """
    Модель для хранения твитов
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(280), nullable=False)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.String, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    images = db.relationship('ImageForTweet', backref='tweet', cascade='all, delete-orphan')


class ImageForTweet(db.Model):
    """
    Модель для хранения данных об изображениях для твитов
    """
    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'))
    path = db.Column(db.String, nullable=True)
