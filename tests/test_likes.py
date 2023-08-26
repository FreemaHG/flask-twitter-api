import pytest

from unittest.mock import patch
from http import HTTPStatus

from app.models.users import User
from app.models.tweets import Tweet, Like

# TODO Пример от препода
class TestApi:

    @pytest.fixture
    def user_model(self) -> User:
        return User(id=1, name="test-user", api_key="test-user")

    @pytest.fixture
    def tweet_model(self) -> Tweet:
        return Tweet(id=1, body="Тестовый твит", user_id=1)

    @patch("app.models.tweets.Like.delete")
    # @patch("app.models.tweets.Like.delete")
    # @patch("app.services.likes.LikesService.delete_like")
    def test_delete_like(self, delete_like_mock, client, user_model, tweet_model):
            like = Like(tweet_id=tweet_model.id, user_id=user_model.id,)

            with (
                    # patch("app.models.users.User.get_by_token", return_value=user_model),
                    patch("app.services.user.UserService.get_user_for_key", return_value=user_model),
                    # patch("app.models.tweets.Like.get_by_ids", return_value=like),
                    patch("app.services.likes.LikesService.check_like_tweet", return_value=like),
            ):
                response = client.delete(
                    "api/tweets/1/likes",
                    headers={"api-key": "test-user"},
                )
            assert response
            assert response.status_code == 200
            assert response.json["result"]
            assert delete_like_mock.called_once()
