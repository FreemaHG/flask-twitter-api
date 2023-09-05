from app import create_app


app = create_app()  # Экземпляр Flask с настройками приложения


if __name__ == "__main__":
    app.run()
