from http import HTTPStatus


class TestToken:

    def test_without_api_key(self, client) -> None:
        """
        Тестирование вывода ошибки при запросе без api-key в header
        """
        resp = client.get("/api/tweets")

        # Ожидаемый ответ
        await_response = {
            "result": False,
            "error_type": f"{HTTPStatus.UNAUTHORIZED}",
            "error_message": "Valid api-token token is missing"
        }

        # Проверка кода ответа - 401
        assert resp.status_code == HTTPStatus.UNAUTHORIZED

        # Проверка ответа
        assert resp.json == await_response


    def test_unidentified_user(self, client) -> None:
        """
        Тестирование вывода ошибки при запросе с api-key в header, но без совпадений в БД
        """
        resp = client.get("/api/tweets", headers={"api-key": "test-user1000"})

        await_response = {
            "result": False,
            "error_type": f"{HTTPStatus.UNAUTHORIZED}",
            "error_message": "Sorry. Wrong api-key token. This user does not exist"
        }

        assert resp.status_code == HTTPStatus.UNAUTHORIZED
        assert resp.json == await_response
