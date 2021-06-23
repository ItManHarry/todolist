from flask import Blueprint, render_template, url_for
bp_auth = Blueprint('auth', __name__)
@bp_auth.route('/login')
def login():
    return render_template('auth/_login.html')