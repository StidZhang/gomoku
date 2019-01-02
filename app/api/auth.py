from . import bp
from werkzeug.security import check_password_hash, generate_password_hash


@bp.route('/login', methods=['GET', 'POST'])
def login():
    return ''
