from flask import send_from_directory
from app import create_app, create_api, STATIC_FOLDER


app = create_app()
rest_api = create_api(app)


@app.route("/<path:path>")
def send_static(path):
    return send_from_directory(STATIC_FOLDER, path)


if __name__ == '__main__':
    app.run()
