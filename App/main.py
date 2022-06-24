from flask import Blueprint, render_template
from flask_login import login_required, current_user
from project import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

from App import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)