from flask import Blueprint, render_template, jsonify, request
from flask_login import login_user, logout_user
from flask_babel import _
from work.models import User
from work.extensions import db
import uuid
bp_auth = Blueprint('auth', __name__)
#登录页面
@bp_auth.route('/login')
def login():
    return render_template('auth/_login.html')
#注册页面
@bp_auth.route('/register')
def register():
    return render_template('auth/_register.html')
#执行注册
@bp_auth.route('/register/exe', methods=['POST'])
def register_exe():
    data = request.get_json()
    code = data['code']
    name = data['name']
    password = data['password']
    print('Code : %s , name %s, password : %s' %(code, name, password))
    if User.query.filter_by(code=code.lower()).first():
        return jsonify(code=0, message=_('user.has.been.exist'))
    user = User(
        id=uuid.uuid4().hex,
        name=name,
        code=code.lower()
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(code=1, message=_('user.register.successfully'))
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