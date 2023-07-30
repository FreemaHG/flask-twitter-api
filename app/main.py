from app import create_app
from app.utils.settings import get_settings


app = create_app(app_settings=get_settings())  # Экземпляр Flask с настройками приложения


if __name__ == "__main__":
    app.run()
