import pytest

from unittest.mock import patch
from http import HTTPStatus

from app.models.users import User
from app.models.tweets import Tweet, Like


# 1 вариант (с твитом)
class TestApi:

    @pytest.fixture
    def user_model(self) -> User:
        return User(id=1, name="test-user", api_key="test-user")

    @pytest.fixture
    def tweet_model(self) -> Tweet:
        return Tweet(id=1, body="Тестовый твит", user_id=1)

    @patch("app.models.tweets.Like.delete")
    def test_delete_like(self, delete_like_mock, client, user_model, tweet_model):
            like = Like(tweet_id=tweet_model.id, user_id=user_model.id)

            with (
                    patch("app.models.users.User.get_by_token", return_value=user_model),
                    patch("app.models.tweets.Like.get_by_ids", return_value=like),
            ):
                response = client.delete(
                    "api/tweets/1/likes",
                    headers={"api-key": "test-user"},
                )
            assert response
            assert response.status_code == 200
            assert response.json["result"]
            assert delete_like_mock.called_once()


# 2 вариант (без твита)
class TestApi2:

    @pytest.fixture
    # 1 - Создали экземпляр пользователя
    def user_model(self):
        return User(id=1, name="TestTest", api_key="test")

    @patch("app.models.tweets.Like.delete")
    def test_delete_like(self, delete_like_mock, client, user_model):
            # 2 - создали экземпляр лайка, который будем удалять
            like = Like(tweet_id=1, user_id=user_model.id)

            with (
                    # 3 - фиктивная проверка, что пользователь аутентифицирован (возвращаем mock-объект)
                    patch("app.models.users.User.get_by_token", return_value=user_model),
                    # 4 - фиктивная проверка, что лайк действительно есть (возвращаем mock-объект)
                    patch("app.models.tweets.Like.get_by_ids", return_value=like),
            ):
                # TODO 5 - Выполняется реальный запрос по URL на удаление, во время которого выполняется запрос к БД
                # TODO и т.к. в БД нет пользователя с api-key == test - тест проваливается из-за исключения 401 UNAUTHORIZED]
                response = client.delete(
                    "api/tweets/1/likes",
                    headers={"api-key": "test"},
                )
            assert response
            # TODO 6 - 401 != 200
            assert response.status_code == 200
            assert response.json["result"]
            assert delete_like_mock.called_once()
