from flask import Blueprint, render_template
api_test = Blueprint('api_text', __name__)
@api_test.route('/')
def index():
    return render_template('api/index.html')