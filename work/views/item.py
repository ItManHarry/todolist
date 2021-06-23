from flask import Blueprint, render_template
bp_item = Blueprint('item', __name__)
#待办事项
@bp_item.route('/todo')
def todo():
    return render_template('item/_todo.html')