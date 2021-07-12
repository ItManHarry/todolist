from webargs import fields, validate, ValidationError
from work.models import User
def check_user_code(code):
    if User.query.first(code.lower()) is not None:
       raise ValidationError('账号已存在!')
user_args = {
    'code': fields.Str(required=True, validate=check_user_code),
    'name': fields.Str(required=True),
    'password': fields.Str(validate=validate.Length(min=6))
}