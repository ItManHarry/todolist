from webargs import fields, validate, ValidationError
from work.models import User
def check_user_code(code):
    user = User.query.filter_by(code=code.lower()).first()
    print('User is >>>>>>>>>>>>>>>>>>>>', user)
    if user is not None:
       raise ValidationError('账号已存在!')
user_args = {
    'code': fields.Str(required=True, validate=[check_user_code, validate.Length(min=1)]),
    'name': fields.Str(required=True, validate=validate.Length(min=1)),
    'password': fields.Str(validate=validate.Length(min=6))
}