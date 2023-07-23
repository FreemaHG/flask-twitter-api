from .routes.users import UserData
from .routes.images import AddImages
from .routes.tweets import TweetsList
from .routes.likes import LikesRoute


# FIXME Добавить схему для URL, чтобы не повторять api в каждом URL
def add_urls(api):
    """
    Функция для регистрации всех URL в API
    """
    api.add_resource(UserData, '/api/users/me', '/api/users/<int:user_id>', endpoint='personal-data')
    api.add_resource(AddImages, '/api/medias', endpoint='add-image')
    api.add_resource(TweetsList, '/api/tweets', '/api/tweets/<int:tweet_id>', endpoint='tweets')
    api.add_resource(LikesRoute, '/api/tweets/<int:tweet_id>/likes', endpoint='like')

    return api

