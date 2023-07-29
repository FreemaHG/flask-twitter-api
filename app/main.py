from app import create_app, create_api, create_swagger
from app.urls import add_urls
# from app.swagger import create_swagger

app = create_app()  # Экземпляр Flask
rest_api = create_api(app)  # Экземпляр Flask RESTApi
rest_api = add_urls(rest_api)  # Регистрация URL
swagger = create_swagger(app=app)  # Подключаем Swagger для автоматической документации


if __name__ == "__main__":
    app.run()
