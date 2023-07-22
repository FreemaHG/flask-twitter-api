from .routes.users import UserData
from .routes.images import AddImages
from .routes.tweets import TweetsList


# FIXME Добавить схему для URL, чтобы не повторять api в каждом URL
def add_urls(api):
    """
    Функция для регистрации всех URL в API
    """
    api.add_resource(UserData, '/api/users/me', '/api/users/<int:user_id>', endpoint='personal-data')
    api.add_resource(AddImages, '/api/medias', endpoint='add-image')
    api.add_resource(TweetsList, '/api/tweets', endpoint='tweets')

    return api

