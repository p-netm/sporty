"""
Defines routes

pages:
1. home page
2. license page/terms and conditions page
"""

from flask import render_template, session, redirect, url_for, request, jsonify
from . import main
from .. import db
from ..gears.tango import get_matches, get_teams
from ..models import Flagged, Team, SubscribedEmail
import datetime, json
from ..email import add_email

def _links():
    """create the filter links name and values,"""
    today = datetime.date.today()
    links_values = [(today + datetime.timedelta(days=counter)).strftime('%Y-%m-%d') for counter in range(-2, 3, 1)]
    markets = ['over', 'under', 'bts yes', 'bts no']
    return [links_values, markets]
    
def get_flagged_fixtures(date_obj, market):
    # date_obj = datetime.date(2018, 6, 26)
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
    result_dict = {'top_ov': get_teams(over=True),
                  'top_un': get_teams(under=True),
                  'top_gg': get_teams(gg=True),
                  'top_ng': get_teams(ng=True)}
    return result_dict

def package():
    links, markets = _links()
    return {
        'dates_nav': links,
        'markets'  : markets,
        'teams_dict_list': teams()
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
            # get the return object as well as  the response  code
            response = add_email(subscribed_email)
            if response['status'] == 'ok':
                return jsonify(response), 200
            else: return jsonify(response), 500
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
