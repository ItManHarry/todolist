from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from work.extensions import db
from work.models import Item
import uuid
bp_item = Blueprint('item', __name__)
#待办事项清单
@bp_item.route('/todo')
def todo():
    items = Item.query.with_parent(current_user).order_by(Item.timestamp.desc()).all()
    print('items : ', len(items))
    return render_template('item/_todo.html', items=items)
#新增/修改事项
@bp_item.route('/item')
def item():
    item_id = request.args.get('itemid', '')
    item = None
    if item_id:
        item = Item.query.get_or_404(item_id)
        print('Title is : ' , item.title)
    return render_template('item/_item.html', item=item)
#执行保存待办事项
@bp_item.route('/save', methods=['POST'])
def save():
    if not current_user.is_active:
        return jsonify(code=0, message='登录超时,请重新登录!')
    data = request.get_json()
    title = data['title']
    body = data['body']
    id = data['id']
    if id:
        item = Item.query.get_or_404(id)
        item.title = title
        item.body = body
    else:
        item = Item(
            id=uuid.uuid4().hex,
            title=title,
            body=body,
            author_id=current_user.id
        )
        db.session.add(item)
    db.session.commit()
    return jsonify(code=1, message='修改成功!' if id else '新增成功!')
#完成待办
@bp_item.route('/finish')
def finish():
    item_id = request.args.get('itemid', '')
    item = Item.query.get_or_404(item_id)
    item.done = True
    db.session.commit()
    return jsonify(code=1, message='待办已完成!')
#删除待办
@bp_item.route('/trash')
def trash():
    item_id = request.args.get('itemid', '')
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify(code=1, message='待办已删除!')