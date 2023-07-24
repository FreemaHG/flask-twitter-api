from app import create_app, create_api
from app.urls import add_urls


app = create_app()  # Экземпляр Flask
rest_api = create_api(app)  # Экземпляр Flask RESTApi
rest_api = add_urls(rest_api)  # Регистрация URL


if __name__ == '__main__':
    app.run()
