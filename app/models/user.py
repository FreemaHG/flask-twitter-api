import datetime

from .. import db


# Подписки пользователей
followers = db.Table(
    'followers',
    db.Column('user_id', db.ForeignKey('user.id'), primary_key=True),
    db.Column('following_user_id', db.ForeignKey('user.id'), primary_key=True)
)


class User(db.Model):
    """
    Модель для хранения данных о пользователях
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    api_key = db.Column(db.String(60))
    password = db.Column(db.String)
    avatar = db.Column(db.String)
    created_at = db.Column(db.String, default=datetime.datetime.now())

    # Многие ко многим (подписки пользователей друг на друга)
    follows = db.relationship(
        'User',
        secondary=followers,
        backref=db.backref('followers', lazy='selectin'),
    )
