from flask_restful import Api

from app.routes.users import UserData, Followers
from app.routes.images import AddImages
from app.routes.tweets import TweetsList, TweetItem
from app.routes.likes import LikesRoute


def add_urls(api: Api) -> Api:
    """
    Функция для регистрации всех URL в Flask RESTApi
    """
    api.add_resource(TweetsList, "/tweets", endpoint="tweets")
    api.add_resource(TweetItem, "/tweets/<int:tweet_id>", endpoint="delete-tweet")
    api.add_resource(AddImages, "/medias", endpoint="add-image")
    api.add_resource(LikesRoute, "/tweets/<int:tweet_id>/likes", endpoint="like")
    api.add_resource(Followers, "/users/<int:user_id>/follow", endpoint="follow")
    api.add_resource(
        UserData, "/users/me", "/users/<int:user_id>", endpoint="personal-data"
    )

    return api
