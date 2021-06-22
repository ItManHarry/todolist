from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from work.extensions import db
'''
    系统用户
'''
class User(db.Model, UserMixin):
    id = db.Column(db.String(32), primary_key=True)                             # ID
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)     # 创建时间
    code = db.Column(db.String(32), unique=True, index=True)                    # 账号
    name = db.Column(db.String(32))                                             # 姓名
    password_hash = db.Column(db.String(128))                                   # 密码
    items = db.relationship('Item', back_populates='author', cascade='all')     # 待办事项

    #使用werkzeug.security提供的加密方式设置密码
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    #校验密码
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
'''
    待办事项
'''
class Item(db.Model):
    id = db.Column(db.String(32), primary_key=True)                             # ID
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)     # 创建时间
    body = db.Column(db.Text)                                                   # 待办事项内容
    done = db.Column(db.Boolean, default=False)                                 # 是否完成
    author_id = db.Column(db.String(32), db.ForeignKey('user.id'))              # 待办事项人ID
    author = db.relationship('User', back_populates='items')                    # 待办事项人(反向关联User)