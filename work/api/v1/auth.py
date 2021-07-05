from flask import current_app, request, g
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as serializer, BadSignature, SignatureExpired
from work.models import User
from work.api.v1.errors import api_abort, invalid_token, token_missing
#生成Token
def generate_token(user):
    expiration = 3600
    s = serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({'id': user.id}).decode('ascii')
    return token, expiration
#获取Token
def get_token():
    if 'Authorization' in request.headers:
        try:
            token_type, token = request.headers['Authorization'].split(None, 1)
        except ValueError:
            token_type = token = None
    else:
        token_type = token = None
    return token_type, token
#验证Token
def validate_token(token):
    s = serializer(current_app.config['SECRET_KEY'])
    try:
       data = s.loads(token)
    except (BadSignature, SignatureExpired):
        return False
    user = User.query.get(data['id'])
    if user is None:
        return False
    g.current_user = user
    return True
#登录保护装饰器
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_type, token = get_token()
        if request.method != 'OPTIONS':
            if token_type is None or token_type.lower() != 'bearer':
                return api_abort(400, message='The token type must be bearer.')
            if token is None:
                return token_missing()
            if not validate_token(token):
                return invalid_token()
        return f(*args, **kwargs)
    return decorated