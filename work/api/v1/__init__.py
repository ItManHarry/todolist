from flask import Blueprint
from flask_cors import CORS
api_v1 = Blueprint('api_v1', __name__)
#添加跨域支持
CORS(api_v1)
from work.api.v1 import resources