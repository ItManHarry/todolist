from flask import jsonify, url_for, g
from flask.views import MethodView
from work.api.v1 import api_v1
from work.models import Item
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
        item = Item.query.get_or_404(item_id)
        #if g.current_user != item.author:
            #return jsonify(code=0, message='Wrong user!')
        return jsonify({
            'id': item.id,
            #'self': url_for('.item', item_id=item.id, _external=True),
            'kind': 'Item',
            'body': item.body,
            'done': item.done,
            'author': {
                'id': item.author.id,
                #'url': url_for('.user', _external=True),
                'username': item.author.name,
                'kind': 'User'
            }
        })
# 添加路由规则
api_v1.add_url_rule('/', view_func=IndexView.as_view('index'), methods=['GET'])
api_v1.add_url_rule('/user/items/<item_id>', view_func=ItemView.as_view('item'), methods=['GET'])