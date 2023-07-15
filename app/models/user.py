import datetime

from ..utils.database import db


class User(db.Model):
    """
    Модель для хранения данных о пользователях
    """
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String, unique=True, nullable=False)
    # TODO Автоматически генерируется из введенного nickname (Cool Dev -> @cooldev)!!!
    username = db.Column(db.String, unique=True, nullable=False)
    api_key = db.Column(db.String)
    password = db.Column(db.String)
    avatar = db.Column(db.String)
    created_at = db.Column(db.String, default=datetime.datetime.now())

    # following = relationship(
    #     "User",
    #     secondary=follows,
    #     primaryjoin=id == follows.c.user_id,
    #     secondaryjoin=id == follows.c.following_user_id,
    #     backref="followers",
    #     lazy="selectin",
    # )

