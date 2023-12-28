from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('weather', __name__)

@bp.route('/')
@bp.route('/home')
def index():
    db=get_db
    return render_template('weather/index.html')


@bp.route('/weather')
def lookup():
    return "looking up weather api here"