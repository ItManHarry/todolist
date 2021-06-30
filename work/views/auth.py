from flask import Blueprint, render_template, jsonify, request
from flask_login import login_user, logout_user
from flask_babel import _
from work.models import User
bp_auth = Blueprint('auth', __name__)
@bp_auth.route('/login')
def login():
    return render_template('auth/_login.html')
@bp_auth.route('/enter', methods=['POST'])
def enter():
    data = request.get_json()
    code = data['code']
    password = data['password']
    user = User.query.filter_by(code=code.lower()).first()
    if user:
        if not user.validate_password(password):
            return jsonify(code=0, message=_('view.auth.wrong.password'))
    else:
        return jsonify(code=0, message=_('view.auth.user.not.exist'))
    login_user(user, True) #交由flask_login管理登录后的信息
    print(_('auth.login.success'))
    return jsonify(code=1, message='OK')
@bp_auth.route('/exit')
def exit():
    logout_user()
    return jsonify(code=1, message=_('view.auth.user.logout'))