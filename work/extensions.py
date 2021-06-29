'''
    Flask扩展
'''
from flask import request, current_app
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user
from flask_babel import Babel
#创建扩展实例
bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
mail = Mail()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()
babel = Babel()
#使用flask_login必须配置此项
@login_manager.user_loader
def load_user(user_id):
    from work.models import User
    user = User.query.get(user_id)
    return user
#设置区域选择函数
@babel.localeselector
def get_locale():
    locale = request.cookies.get('locale')
    if locale is not None:
        return locale
    if current_user.is_authenticated and current_user.locale is not None:
        return current_user.locale
    return request.accept_languages.best_match(current_app.config['SYS_LOCALES'])