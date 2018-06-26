"""
Defines routes

pages:
1. home page
2. lisence page/terms and conditions page
"""

from flask import render_template, session, redirect, url_for, request, jsonify
from . import main
from .. import db
from ..gears.tango import get_matches, get_teams
from ..models import Flagged, Team, SubscribedEmail
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
import datetime, json

def _links():
    """create the filter links name and values,"""
    today = datetime.date.today()
    links_values = [(today + datetime.timedelta(days=counter)).strftime('%Y-%m-%d') for counter in range(-2, 3, 1)]
    markets = ['over', 'under', 'bts yes', 'bts no']
    return [links_values, markets]
    
def get_flagged_fixtures(date_obj, market):
    # remove this***
    date_obj = datetime.date(2018, 6, 26)
    if not isinstance(date_obj, datetime.date):
        raise TypeError('expected {}, got {}'.format('datetime.date', type(date_obj)))
    if market == "over":
        fixtures = get_matches(Flagged, date_obj, over=True)
    if market == "under":
        fixtures = get_matches(Flagged, date_obj, under=True)
    if market == 'bts yes':
        fixtures = get_matches(Flagged, date_obj, gg=True)
    if market == 'bts no':
        fixtures = get_matches(Flagged, date_obj, ng=True)
    return fixtures
    
def teams():
    result_dict = {'top-over': get_teams(over=True),
                  'top_under': get_teams(under=True),
                  'top_gg': get_teams(gg=True),
                  'top_ng': get_teams(ng=True)}
    return result_dict

def package():
    links, markets = _links()
    return {
        'dates_nav': links,
        'markets'  : markets,
        'teams_dict-list': teams()
    }
    

@main.route('/', methods = ['GET', 'POST'])
def index():
    """
    We have an email subscription form and possible sijax integration
    """
    if request.method == 'POST':
        subscribed_email = request.form.get('email')
        full_data = request.form.get('requestData')
        _date = request.form.get("date")
        market = request.form.get("market")


        if full_data:
            return jsonify(package())
        if subscribed_email:
            try:
                new_subscriber = SubscribedEmail(email=subscribed_email)
                db.session.add(new_subscriber)
                db.session.commit()
            except(FlushError, IntegrityError):
                return jsonify({
                    'status': 'bad',
                    'message': 'Email is already subscribed'
                })
            return jsonify({
                'status': 'ok',
                'message': 'Email succesfully subscribed'
            })
        if _date and market:
            # we need to return data for a certain date for the specified market
            date_obj = datetime.datetime.strptime(_date, '%Y-%m-%d')
            return jsonify({
                'tips': get_flagged_fixtures(date_obj, market)
            })

    return render_template('Enhome.html'), 200

@main.route('/terms')
def terms():
    """terms and license page"""
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
        db.session.commit()
