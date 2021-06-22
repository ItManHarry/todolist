'''
    Flask扩展
'''
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
#创建扩展实例
bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
mail = Mail()
migrate = Migrate()
csrf = CSRFProtect()