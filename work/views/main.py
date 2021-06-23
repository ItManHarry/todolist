from flask import Blueprint, render_template
bp_main = Blueprint('main', __name__)
#自我简介
@bp_main.route('/intro')
def intro():
    return render_template('main/_intro.html')