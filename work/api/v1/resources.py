from flask import jsonify
from work.api.v1 import api_v1
@api_v1.route('/')
def index():
    return jsonify(message='Hello , Web API...')