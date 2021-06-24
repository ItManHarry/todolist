'''
    Flask扩展
'''
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
#创建扩展实例
bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
mail = Mail()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()
#使用flask_login必须配置此项
@login_manager.user_loader
def load_user(user_id):
    from work.models import User
    user = User.query.get(user_id)
    return user