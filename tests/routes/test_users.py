import pytest

from http import HTTPStatus


class TestUsers:

    @pytest.fixture
    def response_data(self, good_response):
        """
        Ожидаемый ответ с данными по пользователю
        """
        user_data = {
            "id": 1,
            "name": "test-user1",
            "following": [],
            "followers": [],
        }
        good_response["user"] = user_data
        return good_response

    @pytest.fixture
    def response_error(self, bad_response):
        """
        Ожидаемый ответ в случае запроса не авторизованного пользователя
        """
        bad_response["error_type"] = f"{HTTPStatus.NOT_FOUND}"
        bad_response["error_message"] = "Sorry. This user does not exist"
        return bad_response


    def test_user_me_data(self, client, response_data, users, headers) -> None:
        """
        Тестирование ендпоинта по выводу данных о текущем пользователе
        """
        resp = client.get("/api/users/me", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert resp.json == response_data


    def test_user_data_for_id(self, client, response_data, users, headers) -> None:
        """
        Тестирование ендпоинта по выводу данных о пользователе по переданному id
        """
        resp = client.get("/api/users/1", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert resp.json == response_data


    def test_user_data_for_id_not_found(self, client, response_error, users, headers) -> None:
        """
        Тестирование вывода ошибки при отсутствии пользователя по переданному id
        """
        resp = client.get("/api/users/1000", headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert resp.json == response_error
