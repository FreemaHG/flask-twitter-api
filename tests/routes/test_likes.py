import pytest
from http import HTTPStatus

from app.models.tweets import Like


class TestLikes:
    @pytest.fixture
    def likes(self, users, tweets, db):
        like_1 = Like(user_id=users[0].id, tweet_id=tweets[0].id)
        like_2 = Like(user_id=users[1].id, tweet_id=tweets[1].id)
        db.session.add_all([like_1, like_2])
        db.session.commit()

        return like_1, like_2

    def test_create_like(self, client, likes, headers, good_response) -> None:
        """
        Тестирование добавления лайка к твиту
        """
        resp = client.post("/api/tweets/2/likes", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert resp.json == good_response

    def test_create_like_not_found(
        self, client, likes, headers, response_tweet_not_found
    ) -> None:
        """
        Тестирование вывода ошибки при попытке поставить лайк несуществующему твиту
        """
        resp = client.post("/api/tweets/1000/likes", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert resp.json == response_tweet_not_found

    def test_create_like_locked(self, client, likes, headers, response_locked) -> None:
        """
        Тестирование вывода ошибки при добавлении лайка твиту, у которого уже есть лайк от пользователя
        """
        resp = client.post("/api/tweets/1/likes", headers=headers)
        response_locked["error_message"] = "The user has already liked this tweet"

        assert resp
        assert resp.status_code == HTTPStatus.LOCKED
        assert resp.json == response_locked

    def test_delete_like(self, client, likes, headers, good_response) -> None:
        """
        Тестирование удаления лайка
        """
        resp = client.delete("/api/tweets/1/likes", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert resp.json == good_response

    def test_delete_like_not_found(
        self, client, likes, headers, response_tweet_not_found
    ) -> None:
        """
        Тестирование вывода ошибки при удалении лайка у несуществующей записи
        """
        resp = client.delete("/api/tweets/1000/likes", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert resp.json == response_tweet_not_found

    def test_delete_like_locked(self, client, likes, headers, response_locked) -> None:
        """
        Тестирование вывода ошибки при попытке удалить не существующий лайк
        """
        resp = client.delete("/api/tweets/2/likes", headers=headers)
        response_locked["error_message"] = "The user has not yet liked this tweet"

        assert resp
        assert resp.status_code == HTTPStatus.LOCKED
        assert resp.json == response_locked
