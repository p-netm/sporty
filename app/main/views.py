"""
Defines routes

pages:
1. home page
2. lisence page/terms and conditions page
"""

from flask import render_template, session, redirect, url_for, request, jsonify
from . import main
from .. import db
from ..models import Flagged, Team, SubscribedEmail
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
import datetime, json

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
    result_dict = {'top-over': top_over,
                  'top_under': top_under,
                  'top_gg': top_gg,
                  'top_ng': top_ng}
    return result_dict
    

@main.route('/', methods = ['GET', 'POST'])
def index():
    """
    We have an email subscription form and possible sijax integration
    """
    
    json_bytes = request.get_data()
    json_data = (json_bytes.decode('utf-8'))
    if request.method == 'POST':
        print(json_data)
        import pdb; pdb.set_trace()
        subscribed_email = json_data
        if subscribed_email is not None:
            try:
                raise KeyError
                new_subscriber = SubscribedEmail(email=subscribed_email)
                db.session.add(new_subscriber)
                db.session.commit()
            except(FlushError, IntegrityError, KeyError):
                jsonify({
                'message': 'Email is already subscribed'
            })
            return jsonify({
                'message': 'Email succesfully subscribed'
            })
    return render_template('email.html'), 200

@main.route('/terms')
def terms():
    """terms and lisence page"""
    pass

@main.route('/unsubscribe/<token>')
def unsubscribe(token):
    #unserialize token into email
    # ** error when trying to install jwt
    email_string = token
    res = SubscribedEmail.query.filter_by(email=email_string).first()
    if res is None:
        #log error
        pass
    else:
        SubscribedEmail.remove(res)
        db.session
