import pytest

from http import HTTPStatus


class TestFollowers:

    @pytest.fixture
    def followers(self, users, db):
        users[0].following.append(users[1])
        users[1].following.append(users[2])
        db.session.add_all([users[0], users[1]])

    @pytest.fixture
    def response_not_user(self, response_not_found):
        response_not_found['error_message'] = 'The subscription user was not found'
        return response_not_found

    @pytest.fixture
    def response_existing_subscription(self, response_locked):
        response_locked['error_message'] = 'The subscription has already been issued'
        return response_locked

    @pytest.fixture
    def response_subscription_not_found(self, response_not_found):
        response_not_found['error_message'] = 'The user to cancel the subscription was not found'
        return response_not_found

    @pytest.fixture
    def response_among_subscribers(self, response_locked):
        response_locked['error_message'] = 'The user is not among the subscribers'
        return response_locked


    def test_create_follower(self, client, followers, headers, good_response) -> None:
        """
        Тестирование подписки на пользователя
        """
        resp = client.post('/api/users/3/follow', headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.CREATED
        assert resp.json == good_response


    def test_create_follower_not_found(self, client, followers, headers, response_not_user) -> None:
        """
        Тестирование вывода ошибки при попытке подписки на несуществующего пользователя
        """
        resp = client.post('/api/users/1000/follow', headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert resp.json == response_not_user


    def test_create_follower_locked(self, client, followers, headers, response_existing_subscription) -> None:
        """
        Тестирование вывода ошибки при попытке подписки на уже подписанного ранее пользователя
        """
        resp = client.post('/api/users/2/follow', headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.LOCKED
        assert resp.json == response_existing_subscription


    def test_delete_follower(self, client, followers, headers, good_response) -> None:
        """
        Тестирование удаления подписки пользователя
        """
        resp = client.delete('/api/users/2/follow', headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.OK
        assert resp.json == good_response


    def test_delete_follower_not_found(self, client, followers, headers, response_subscription_not_found) -> None:
        """
        Тестирование вывода ошибки при удалении подписки с несуществующего пользователя
        """
        resp = client.delete('/api/users/1000/follow', headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.NOT_FOUND
        assert resp.json == response_subscription_not_found


    def test_delete_follower_locked(self, client, followers, headers, response_among_subscribers) -> None:
        """
        Тестирование вывода ошибки при удалении подписки от пользователя, на которого нет подписки
        """
        resp = client.delete('/api/users/3/follow', headers=headers)

        assert resp
        assert resp.status_code == HTTPStatus.LOCKED
        assert resp.json == response_among_subscribers
