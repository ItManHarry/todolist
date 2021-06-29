from flask import Blueprint, render_template, current_app, jsonify, make_response
from flask_login import current_user
from work.extensions import db
bp_main = Blueprint('main', __name__)
#自我简介
@bp_main.route('/intro')
def intro():
    return render_template('main/_intro.html')
#国际化设置
@bp_main.route('/set_locale/<locale>')
def set_locale(locale):
    if locale not in current_app.config['SYS_LOCALES']:
        return jsonify(code=0, message='区域代码不存在!')
    if current_user.is_authenticated:
        current_user.locale = locale
        db.session.commit()
    response = make_response(jsonify(code=1, message='区域代码已更新!'))
    response.set_cookie('locale', locale, max_age=60 * 60 * 24 * 30)
    return response