from flask import jsonify, url_for, g, request
from flask.views import MethodView
from work.api.v1 import api_v1
from work.models import Item
from work.extensions import db
from work.api.v1.schemas import item_schema
from work.api.v1.errors import ValidationError
class IndexView(MethodView):
    def get(self):
        return jsonify({
            "api_version": "1.0",
            "api_base_url": "http://todolist.cn/api/v1",
            "current_user_url": "http://todolist.cn/api/v1/user",
            "authentication_url": "http://todolist.cn/api/v1/token",
            "item_url": "http://todolist.cn/api/v1/items/{item_id}",
            "current_user_items_url": "http://todolist.cn/api/v1/user/items{?page, per_page}",
            "current_user_active_items_url": "http://todolist.cn/api/v1/user/items/active{?page, per_page}",
            "current_user_completed_items_url": "http://todolist.cn/api/v1/user/items/completed{?page, per_page}"
        })
class ItemView(MethodView):
    def get(self, item_id):
        #获取待办事项
        item = Item.query.get_or_404(item_id)
        #if g.current_user != item.author:
            #return jsonify(code=0, message='Wrong user!')
        return jsonify(item_schema(item))
    #修改待办事项
    def put(self, item_id):
        item = Item.query.get_or_404(item_id)
        item.title = get_item_values()['title']
        item.body = get_item_values()['body']
        db.session.commit()
        return jsonify(code=1, message='待办事项信息更新成功!')
def get_item_values():
    data = request.get_json()
    title = data['title']
    body = data['body']
    if title is None or str(title).strip() == '':
        raise ValidationError('待办事项标题为空或者为传递!')
    if body is None or str(body).strip() == '':
        raise ValidationError('待办事项内容为空或者为传递!')
    return {
        'title': title,
        'body': body
    }
# 添加路由规则
api_v1.add_url_rule('/', view_func=IndexView.as_view('index'), methods=['GET'])
api_v1.add_url_rule('/user/items/<item_id>', view_func=ItemView.as_view('item'), methods=['GET', 'PUT'])