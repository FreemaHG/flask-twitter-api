from loguru import logger

from app.main import app
from app.database import db
from app.models.users import User
from app.models.tweets import Tweet, Image, Like


users = [
    {
        "name": "Дмитрий",
        "api_key": "test",
    },
    {
        "name": "Елена",
        "api_key": "test2",
    },
    {
        "name": "Анастасия",
        "api_key": "test3",
    },
]

images = [
    {
        "tweet_id": 1,
        "path": "images/tweets/migrations_img/1.jpeg",
    },
    {
        "tweet_id": 4,
        "path": "images/tweets/migrations_img/3.png",
    },
    {
        "tweet_id": 6,
        "path": "images/tweets/migrations_img/5.jpeg",
    },
    {
        "tweet_id": 6,
        "path": "images/tweets/migrations_img/7.jpeg",
    },
    {
        "tweet_id": 6,
        "path": "images/tweets/migrations_img/2.jpeg",
    },
    {
        "tweet_id": 8,
        "path": "images/tweets/migrations_img/4.png",
    },
    {
        "tweet_id": 11,
        "path": "images/tweets/migrations_img/6.jpeg",
    },
    {
        "tweet_id": 10,
        "path": "images/tweets/migrations_img/8.jpeg",
    },
]

tweets = [
    {
        "body": "Это я в ожидании своего отпуска )",
        "user_id": 1,
    },
    {
        "body": "Похоже снова придется наслаждаться конфетами",
        "user_id": 2,
    },
    {
        "body": "Кто сколько сбросил к Новому Году?",
        "user_id": 3,
    },
    {
        "body": "Очередной утомительный созвон на работе (((",
        "user_id": 2,
    },
    {
        "body": "Очаровательный получился подарок!!!",
        "user_id": 1,
    },
    {
        "body": "Предыдущий отпуск провели на отлично!",
        "user_id": 1,
    },
    {
        "body": "Кто знает, откуда это состояние?",
        "user_id": 3,
    },
    {
        "body": "Только посмотрите, кого я завела...",
        "user_id": 3,
    },
    {
        "body": "Интересно, почему чем больше денег, тем сумка кажется легче...",
        "user_id": 2,
    },
    {
        "body": "У меня тоже новый приятель )",
        "user_id": 2,
    },
    {
        "body": "Когда просишь у начальства зарплаты ))",
        "user_id": 2,
    },
    {
        "body": "Кто-нибудь уже приступил к квартальному отчету?",
        "user_id": 1,
    },
]

likes = [
    {
        "user_id": 1,
        "tweet_id": 1,
    },
    {
        "user_id": 3,
        "tweet_id": 1,
    },
    {
        "user_id": 2,
        "tweet_id": 1,
    },
    {
        "user_id": 2,
        "tweet_id": 2,
    },
    {
        "user_id": 3,
        "tweet_id": 2,
    },
    {
        "user_id": 1,
        "tweet_id": 3,
    },
    {
        "user_id": 2,
        "tweet_id": 3,
    },
    {
        "user_id": 1,
        "tweet_id": 4,
    },
    {
        "user_id": 1,
        "tweet_id": 6,
    },
    {
        "user_id": 3,
        "tweet_id": 6,
    },
    {
        "user_id": 2,
        "tweet_id": 7,
    },
    {
        "user_id": 1,
        "tweet_id": 9,
    },
    {
        "user_id": 2,
        "tweet_id": 9,
    },
    {
        "user_id": 2,
        "tweet_id": 11,
    },
    {
        "user_id": 3,
        "tweet_id": 11,
    },
]


def re_creation_db():
    """
    Удаление и создание БД
    """
    logger.debug("Создание БД")

    with app.app_context():
        db.drop_all()  # Удаление всех таблиц
        db.create_all()  # Создание всех таблиц


def migration_data():
    """
    Функция для наполнения БД демонстрационными данными
    """
    logger.debug("Загрузка демонстрационных данных")

    re_creation_db()

    with app.app_context():
        # Инициализируем и добавляем пользователей
        initial_users = [User(**user) for user in users]
        db.session.add_all(initial_users)

        # Подписки пользователей
        initial_users[0].following.extend([initial_users[1], initial_users[2]])
        initial_users[1].following.append(initial_users[0])
        initial_users[2].following.extend([initial_users[1], initial_users[0]])

        # Твиты
        initial_tweets = [Tweet(**tweet) for tweet in tweets]
        db.session.add_all(initial_tweets)

        # Изображения к твитам
        initial_images = [Image(**image) for image in images]
        db.session.add_all(initial_images)

        # Лайки
        initial_likes = [Like(**like) for like in likes]
        db.session.add_all(initial_likes)

        db.session.commit()

        logger.debug("Данные успешно добавлены")


if __name__ == "__main__":
    migration_data()
