from .routes.users import UserData


def add_urls(api):
    """
    Функция для регистрации всех URL в API
    """
    api.add_resource(UserData, '/api/users/me', '/api/users/<int:user_id>', endpoint='personal-data')

    return api
