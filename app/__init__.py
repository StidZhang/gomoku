import os
from flask import Flask, send_file, request, jsonify
from flask_login import LoginManager
from flask_socketio import SocketIO


def create_app():
    app = Flask(__name__, static_folder='../dist', static_url_path='')

    from .config import Config
    app.config.from_object(Config)

    @app.route('/')
    @app.errorhandler(404)
    def index(e=None):
        if request.path.startswith('/api/'):
            return jsonify(status=404), 404
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

    from .gomoku import GomokuSocket
    socketio.on_namespace(GomokuSocket())

    return app
