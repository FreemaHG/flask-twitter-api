import json
from http import HTTPStatus
import pytest


class TestTweets:
    @pytest.fixture
    def headers_with_content_type(self, headers):
        """
        Заголовок при добавлении нового твита
        """
        headers["Content-Type"] = "application/json"
        return headers

    @pytest.fixture
    def resp_for_new_tweet(self, good_response):
        """
        Успешный ответ при добавлении нового твита
        """
        good_response["tweet_id"] = 3
        return good_response

    @pytest.fixture
    def new_tweet(self):
        """
        Данные для добавления нового твита
        """
        return {"tweet_data": "Тестовый твит", "tweet_media_ids": []}

    @pytest.fixture
    def new_tweet_with_image(self, new_tweet):
        """
        Данные для добавления нового твита с изображениями
        """
        new_tweet["tweet_media_ids"] = [1, 2]
        return new_tweet

    @pytest.fixture
    def response_tweet_locked(self, response_locked):
        response_locked["error_message"] = "The tweet that is being accessed is locked"
        return response_locked

    def send_request(self, client, headers, new_tweet_data=new_tweet):
        """
        Отправка запроса на добавление нового твита
        """
        resp = client.post(
            "/api/tweets", data=json.dumps(new_tweet_data), headers=headers
        )

        return resp

    def test_create_tweet(
        self, client, tweets, new_tweet, headers_with_content_type, resp_for_new_tweet
    ) -> None:
        """
        Тестирование добавления твита (без изображений)
        """
        resp = self.send_request(
            client=client, headers=headers_with_content_type, new_tweet_data=new_tweet
        )

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert resp.json == resp_for_new_tweet

    def test_create_tweet_with_images(
        self,
        client,
        tweets,
        headers_with_content_type,
        new_tweet_with_image,
        resp_for_new_tweet,
    ) -> None:
        """
        Тестирование добавления твита с изображениями
        """
        resp = self.send_request(
            client=client,
            headers=headers_with_content_type,
            new_tweet_data=new_tweet_with_image,
        )
        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert resp.json == resp_for_new_tweet

    def test_create_invalid_tweet(
        self,
        client,
        tweets,
        headers_with_content_type,
        new_tweet,
        resp_for_new_tweet,
        bad_response,
    ) -> None:
        """
        Тестирование вывода сообщения об ошибке при публикации слишком длинного твита (> 280 символов)
        """
        new_tweet["tweet_data"] = (
            "Python — идеальный язык для новичка. "
            "Код на Python легко писать и читать, язык стабильно занимает высокие места "
            "в рейтингах популярности, а «питонисты» востребованы почти во всех сферах "
            "IT — программировании, анализе данных, системном администрировании и тестировании. "
            "YouTube, Intel, Pixar, NASA, VK, Яндекс — вот лишь немногие из известных компаний, "
            "которые используют Python в своих продуктах."
        )

        resp = self.send_request(
            client=client, headers=headers_with_content_type, new_tweet_data=new_tweet
        )

        bad_response["error_type"] = f"{HTTPStatus.BAD_REQUEST}"
        bad_response["error_message"] = (
            "The length of the tweet should not exceed 280 characters. "
            f"Current value: {len(new_tweet['tweet_data'])}"
        )

        assert resp
        assert resp.status_code == HTTPStatus.BAD_REQUEST
        assert resp.json == bad_response

    def test_delete_tweet(self, client, tweets, headers, good_response) -> None:
        """
        Тестирование удаление твита
        """
        resp = client.delete("/api/tweets/1", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert resp.json == good_response

    def test_delete_tweet_not_found(
        self, client, tweets, headers, response_tweet_not_found
    ) -> None:
        """
        Тестирование вывода ошибки при попытке удалить несуществующий твит
        """
        resp = client.delete("/api/tweets/1000", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert resp.json == response_tweet_not_found

    def test_delete_tweet_locked(
        self, client, tweets, headers, response_tweet_locked
    ) -> None:
        """
        Тестирование вывода ошибки при попытке удалить чужой твит
        """
        resp = client.delete("/api/tweets/2", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.LOCKED
        assert resp.json == response_tweet_locked
