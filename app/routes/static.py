from flask import send_from_directory
from app import STATIC_FOLDER
from app.main import app


@app.route("/<path:path>")
def send_static(path):
    """
    Вывод статических файлов
    """
    return send_from_directory(STATIC_FOLDER, path)
