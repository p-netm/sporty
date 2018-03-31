"""
Defines routes

pages:
1 home page
2 contact page
3 licence page
4. terms and conditions page
"""

from flask import render_template, session, redirect, url_for, request
from . import main
from .forms import Email
from .. import db
from ..models import *

@main.route('/')
def index():
    """We have an email subscription form and possible sijax integration
   """
    return render_template('home.html'), 200