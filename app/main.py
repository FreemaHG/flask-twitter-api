from flask import send_from_directory
from app import create_app, STATIC_FOLDER


app = create_app()


@app.route("/<path:path>")
def send_static(path):
    return send_from_directory(STATIC_FOLDER, path)


if __name__ == '__main__':
    app.run()
