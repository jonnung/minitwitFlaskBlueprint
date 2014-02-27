# -*- coding: utf-8 -*-

from flask import render_template
from flask.blueprints import Blueprint


bp_minitwit = Blueprint('bp_minitwit', __name__)

@bp_minitwit.route('/')
def timeline():
    return render_template('timeline.html')

