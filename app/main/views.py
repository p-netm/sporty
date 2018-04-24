"""
Defines routes

pages:
1. home page
2. lisence page/terms and conditions page
"""

from flask import render_template, session, redirect, url_for, request
from . import main
from .forms import Email
from .. import db
from ..models import Flagged, Team, SubscribedEmail
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
import datetime

def links():
    """create the filter links name and values,"""
    today = datetime.date.today()
    links_values = [today + datetime.timedelta(days=counter) for counter in range(-3,4,1)]
    markets = ['over', 'under', 'bts yes', 'bts no']
    
def get_flagged_fixtures(date_obj):
    if not isinstance(date_obj, datetime.date):
        raise TypeError('expected {}, got {}'.format('datetime.date','type(date_obj)'))
    fixtures = Flagged.query.filter(Flagged.date == date_obj).all()
    
def get_teams(market):
    top_over = Team.query.filter(Team.ov == True).all()
    top_under = Team.query.filter(Team.un == True).all()
    top_gg = Team.query.filter(Team.gg == True).all()
    top_ng = Team.query.filter(Team.ng == True).all()
    

@main.route('/')
def index():
    """
    We have an email subscription form and possible sijax integration
    """
    email_form = Email()
    if email_form.validate_on_submit and email_form.submit.data:
        subscribed_email = email_form.email.data
        try:
            new_subscriber = SubscribedEmail(email=subscribed_email)
            db.session.add(new_subscriber)
            db.session.commit()
        except(FlushError, IntegrityError):
            flash("the email is already subscribed")
    return render_template('home.html'), 200

@main.route('/terms')
def terms():
    """terms and lisence page"""
    pass

@main.route('/unsubscribe/<token>'):
    def unsubscribe(token):
        #unserialize token into email
        email_string = 
        res = SubscribedEmail.query.filter_by(email=email_string).first()
        if res is None:
            #log error
            pass
        else:
            SubscribedEmail.remove(res)
            db.session
            