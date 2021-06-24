from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from work.extensions import db
from work.models import Item
import uuid
bp_item = Blueprint('item', __name__)
#待办事项
@bp_item.route('/todo')
def todo():
    items = Item.query.with_parent(current_user).order_by(Item.timestamp.desc()).all()
    print('items : ', len(items))
    return render_template('item/_todo.html', items=items)
#新增/修改事项
@bp_item.route('/item')
def item():
    return render_template('item/_item.html')
@bp_item.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    title = data['title']
    body = data['body']
    item = Item(
        id=uuid.uuid4().hex,
        title=title,
        body=body,
        author_id=current_user.id
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(code=1, message='添加成功!!!')