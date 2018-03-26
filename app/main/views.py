"""
Defines visible content

pages:
1 home page
2 contact page
3 administration panel page
"""

from flask import render_template, session, redirect, url_for
from . import main
from .. import db
from ..models import *

@main.route('/')
def index():
    return render_template('index.html'), 200