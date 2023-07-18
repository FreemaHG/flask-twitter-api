import os

from flask import render_template, send_from_directory

from app import create_app


root_dir = os.path.dirname(os.path.abspath(__file__))
template_folder = os.path.join(root_dir, "templates")
static_folder = os.path.join(root_dir, "static")


app = create_app()


# from flask import send_from_directory, url_for
#
# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory(static_folder, path)


if __name__ == '__main__':
    app.run()
