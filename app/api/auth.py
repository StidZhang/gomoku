from . import bp
from flask import jsonify, request, abort
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from ..user import User, get_user_by_name, create_user, change_user_password


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        content = request.get_json(force=True)
        if content is None:
            return abort(403)

        username = content.get('username', None)
        password = content.get('password', None)

        if not username or not password:
            return abort(403)

        u = get_user_by_name(username)
        if u is None:
            return jsonify(status=-1, message="User does not exists")
        elif not check_password_hash(u['password'], password):
            return jsonify(status=-1, message="Password is not correct")

        login_user(User(u))
        return jsonify(status=0, username=username)
    else:
        if current_user.is_authenticated:
            return jsonify(status=0, username=current_user.username)
        else:
            return jsonify(status=-1, message='Not logged in')


@bp.route('/register', methods=['POST'])
def register():
    content = request.get_json(force=True)
    if content is None:
        return abort(403)

    username = content.get('username', None)
    password = content.get('password', None)

    if not username or not password:
        return abort(403)

    u = get_user_by_name(username)
    if u is not None:
        return jsonify(status=-1, message="User already exists")

    u = create_user(username, generate_password_hash(password))
    login_user(User(u))
    return jsonify(status=0, username=username)


@bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify(status=0)


@bp.route('/changepasswd', methods=['GET'])
def changepasswd():
    content = request.get_json(force=True)
    if content is None:
        return abort(403)

    username = content.get('username', None)
    password = content.get('password', None)
    newpass = content.get('newpass', None)
    if not username or not password or not newpass:
        return abort(403)

    u = get_user_by_name(username)
    if u is None:
        return jsonify(status=-1, message='User does not exists.')
    elif not check_password_hash(u['password'], password):
        return jsonify(status=-1, message='Password not match.')

    change_user_password(u['_id'], generate_password_hash(newpass))
    return jsonify(status=0, username=username)
