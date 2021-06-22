from flask import Flask, render_template
from flask_wtf.csrf import CSRFError
from work.settings import config
from work.extensions import bootstrap, db, moment, mail, migrate, csrf
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
    register_app_shell(app)
    return app
#注册系统组件
def register_app_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    migrate.init_app(app)
    csrf.init_app(app)
#配置全局路径
def register_app_global_path(app):
    @app.route('/index')
    def index():
        return '<h1>To to list ...</h1>'
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
#配置shell环境
def register_app_shell(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)