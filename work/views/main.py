from flask import Blueprint, render_template
bp_main = Blueprint('main', __name__)
#系统主页
@bp_main.route('/index')
def index():
    return render_template('index.html')