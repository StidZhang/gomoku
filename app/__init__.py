import os
from flask import Flask, send_file
from flask_login import LoginManager
from flask_socketio import SocketIO


def create_app():
    from .config import Config
    app = Flask(__name__, static_folder='../dist', static_url_path='')
    app.config.from_mapping(
        SECRET_KEY=Config.SECRET_KEY
    )

    @app.route('/')
    @app.errorhandler(404)
    def index(e=None):
        entry = os.path.join('../dist', 'index.html')
        return send_file(entry)

    from . import api
    app.register_blueprint(api.bp)

    from . import db
    db.init_app(app)

    from .user import get_user_by_name, User
    login_manager = LoginManager()

    @login_manager.user_loader
    def load_user(user_id):
        u = get_user_by_name(user_id)
        return User(u) if u is not None else None

    login_manager.init_app(app)
    socketio = SocketIO(app)

    return app
