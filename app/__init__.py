import os
from flask import Flask, send_file


def create_app():
    app = Flask(__name__, static_folder='../dist', static_url_path='')

    @app.route('/')
    def index():
        entry = os.path.join('../dist', 'index.html')
        return send_file(entry)

    from . import api
    app.register_blueprint(api.bp)

    return app
