from sqlalchemy import func

from app.database import db

class Tweet(db.Model):
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

class Image(db.Model):
    """
    Модель для хранения изображений
    """

    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey("tweet.id"), nullable=True)
    path = db.Column(db.String, nullable=True)

class Like(db.Model):
    """
    Модель для хранения данных о лайках
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    tweet_id = db.Column(db.Integer, db.ForeignKey("tweet.id"))
