from flask import jsonify, url_for, g, request, current_app
from flask.views import MethodView
from work.api.v1 import api_v1
from work.models import Item, User
from work.extensions import db
from work.api.v1.schemas import item_schema, items_schema
from work.api.v1.errors import ValidationError, api_abort
from work.api.v1.auth import generate_token, auth_required
import uuid
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
    decorators = [auth_required]
    def get(self, item_id):
        #获取待办事项
        item = Item.query.get_or_404(item_id)
        if g.current_user != item.author:
            return jsonify(code=0, message='Wrong user!')
        return jsonify(item_schema(item))
    #新增待办事项
    def post(self):
        title = get_item_values()['title']
        body = get_item_values()['body']
        item = Item(
            id=uuid.uuid4().hex,
            title=title,
            body=body,
            author_id=g.current_user.id
        )
        db.session.add(item)
        db.session.commit()
        return jsonify(code=1, message='待办事项信息新增成功!')
    # 修改待办事项
    def put(self, item_id):
        item = Item.query.get_or_404(item_id)
        if g.current_user != item.author:
            return jsonify(code=0, message='Wrong User!')
        item.title = get_item_values()['title']
        item.body = get_item_values()['body']
        db.session.commit()
        return jsonify(code=1, message='待办事项信息更新成功!')
    #更改完成状态
    def patch(self, item_id):
        item = Item.query.get_or_404(item_id)
        if g.current_user != item.author:
            return jsonify(code=1, message='Wrong User!')
        item.done = not item.done
        db.session.commit()
        return jsonify(code=1, message='待办事项完成状态更改成功!')
    #删除待办
    def delete(self, item_id):
        item = Item.query.get_or_404(item_id)
        if g.current_user != item.author:
            return jsonify(code=1, message='Wrong User!')
        db.session.delete(item)
        db.session.commit()
        return jsonify(code=1, message='待办事项删除成功!')
def get_item_values():
    data = request.get_json()
    title = data['title']
    body = data['body']
    if title is None or str(title).strip() == '':
        raise ValidationError('待办事项标题为空或者未传递!')
    if body is None or str(body).strip() == '':
        raise ValidationError('待办事项内容为空或者未传递!')
    return {
        'title': title,
        'body': body
    }
class AuthTokenAPI(MethodView):
     def post(self):
         grant_type = request.form.get('grant_type')
         username = request.form.get('username')
         password = request.form.get('password')
         if grant_type is None or grant_type.lower() != 'password':
             return api_abort(400, message='The grant type must be password.')
         user = User.query.filter_by(name=username).first()
         if user is None or not user.validate_password(password):
             return api_abort(400, message='User name or password is not right.')
         token, expiration = generate_token(user)
         response = jsonify({
             'access_token': token,
             'token_type': 'Bearer',
             'expires_in': expiration
         })
         response.headers['Cache-Control'] = 'no-store'
         response.headers['Pragma'] = 'no-cache'
         return response
#分页获取记录
@api_v1.route('/item/pages', methods=['GET'])
@auth_required
def item_pages():
    #分页获取待办事项
    page = request.args.get('page', 1, type=int)
    pagination = Item.query.with_parent(g.current_user).paginate(page, per_page=current_app.config['TODO_ITEM_PER_PAGE'])
    items = pagination.items
    data = items_schema(items, pagination)
    #print('Items size is : ', len(items), ', and data is : ', data)
    return jsonify(data)
# 用户注册-传参方式一
from webargs.flaskparser import parser
from work.api.v1.args import user_args
@api_v1.route('/user/register1', methods=['POST'])
def register1():
    print('Do the user register action now...')
    args = parser.parse(user_args, request)
    user = User(
        id=uuid.uuid4().hex,
        code=args['code'].lower(),
        name=args['name']
    )
    user.set_password(args['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(code=1, message='用户注册成功!')
# 传参方式二
from webargs.flaskparser import use_args
@api_v1.route('/user/register2', methods=['POST'])
@use_args(user_args)
def register2(args):
    user = User(
        id=uuid.uuid4().hex,
        code=args['code'].lower(),
        name=args['name']
    )
    user.set_password(args['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(code=1, message='用户注册成功!')
# 传参方式三
from webargs.flaskparser import use_kwargs
@api_v1.route('/user/register3', methods=['POST'])
@use_kwargs(user_args)
def register3(code, name, password):
    u = User.query.filter_by(code=code.lower()).first()
    if u is None:
        print('User is not Exist!!!')
    else:
        print('User has been Exist!!!')
        return jsonify(code=0, message='用户代码已存在!')
    user = User(
        id=uuid.uuid4().hex,
        code=code.lower(),
        name=name
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(code=1, message='用户注册成功!')
# 添加路由规则
api_v1.add_url_rule('/', view_func=IndexView.as_view('index'), methods=['GET'])
api_v1.add_url_rule('/oauth/token', view_func=AuthTokenAPI.as_view('token'), methods=['POST'])
api_v1.add_url_rule('/user/items/add', view_func=ItemView.as_view('item-add'), methods=['POST'])
api_v1.add_url_rule('/user/items/<item_id>', view_func=ItemView.as_view('item-update'), methods=['GET', 'PUT', 'PATCH', 'DELETE'])