from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

todo = Blueprint('todo', __name__, template_folder='templates')

@todo.route('/home')
def home():
    try:
        return render_template('home.html')
    except TemplateNotFound:
        abort(404)