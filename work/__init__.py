from flask import Flask, render_template, redirect, url_for
from flask_wtf.csrf import CSRFError
from work.settings import config
from work.extensions import bootstrap, db, moment, mail, migrate, csrf, login_manager
import click
import uuid
#创建Flask实例
def create_app(config_name=None):
    if config_name == None:
        config_name = 'dev_config'
    #创建实例
    app = Flask('work')
    #加载配置
    app.config.from_object(config[config_name])
    #注册组件等
    register_app_extensions(app)
    register_app_global_path(app)
    register_app_global_context(app)
    register_app_error_pages(app)
    register_app_views(app)
    register_app_shell(app)
    register_app_command(app)
    return app
#注册系统组件
def register_app_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    migrate.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
#配置全局路径
def register_app_global_path(app):
    @app.route('/')
    def index():
        return render_template('index.html')
#配件全局函数/变量
def register_app_global_context(app):
    from work.tools import get_time
    @app.context_processor
    def make_context_processor():
        return dict(get_time=get_time)
#配置系统错误页面
def register_app_error_pages(app):
    @app.errorhandler(400)
    def request_invalid(e):
        return render_template('errors/400.html'), 400
    @app.errorhandler(403)
    def request_invalid(e):
        return render_template('errors/403.html'), 403
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    @app.errorhandler(500)
    def inner_error(e):
        return render_template('errors/500.html'), 500
    @app.errorhandler(CSRFError)
    def csrf_error(e):
        return render_template('errors/csrf.html')
#配置系统功能模块
def register_app_views(app):
    from work.views.auth import bp_auth
    from work.views.main import bp_main
    from work.views.item import bp_item
    app.register_blueprint(bp_auth, url_prefix='/auth')
    app.register_blueprint(bp_main, url_prefix='/main')
    app.register_blueprint(bp_item, url_prefix='/item')
#配置shell环境
def register_app_shell(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)
#配置系统自定义命令
def register_app_command(app):
    #初始化系统
    @app.cli.command()
    @click.option('--username', prompt=True, help='管理员账号......')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='管理员密码......')
    def init(username, password):
        from work.models import User
        click.echo('执行数据库初始化......')
        db.create_all()
        click.echo('数据库初始化完成......')
        click.echo('创建系统管理员......')
        user = User.query.first()
        if user:
            click.echo('管理员已存在, 无需创建')
        else:
            user = User(
                id = uuid.uuid4().hex,
                code = username.lower(),
                name = username.lower()
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            click.echo('系统管理员创建完成......')
        click.echo('系统初始化完成......')