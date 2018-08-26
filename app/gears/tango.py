"""
Tango is where operation controls happen, defined here, you will find
methods ready to initialise the scrap engine, save the data in our trusty
databases and then invoke the evaluator on the saved data
"""
from ..models import *
from .scrapper import _run_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
import datetime
from .analyser import gg, ng, ov, un, top_team
from sqlalchemy import desc


def saver(url="""http://www.sportstats.com/soccer/matches/"""):
    """Officer in charge of defensive operations, commands the scrap functions
    to go and get data, in other words you could say he is in charge of reconnaisance
    :parameters: specific url to scrap from, the urls only defer in date
    :returns: boolean value or flags an error if it runs into one"""
    results = _run_(url)
    data = results['full_data']
    for diction in data:
        saver_worker(diction)
        for semi_diction in diction['mutual']:
            saver_worker(semi_diction)
    return


def saver_worker(diction):
    """saver subcommandant incharge of data verification and the actual work of saving.
    makes sure we do not have redundant info being added  to our databases
    :parameters: one diction instance without any further nested match objects
    presence of usch objects e.g. lists and dictions will be ignored"""
    # counries have unique names
    # leagues may have similar names but not in the same country
    # teams may have similar names but not in the same league(i hope)
    try:
        return save_match(diction)
    except KeyError as e:
        return


def save_country(country):
    """:paramter: a string variable of the country name to be saved
    :returns: created object at successful completion of the operation, otherwise will return False
    if the country is already existent
    """
    try:
        country_obj = Country(country_name=country)
        db.session.add(country_obj)
        db.session.commit()
        return country_obj
    except (IntegrityError, FlushError) as e:
        db.session.rollback()
        return False


def save_league(country, league):
    """
    :parameters: the country_name and the league name
    :returns: True if the league is succesfully added and linked to a country
    false if the league already exists
    """
    try:
        league_obj = League(country_name=country, league_name=league)
        db.session.add(league_obj)
        db.session.commit()
        return league_obj
    except IntegrityError as error:
        db.session.rollback()
        return False


def save_team(team, logo=None):
    """
    :parameters:  the team_name, all as string
    :returns Boolean if operation successful otherwise false if team already existent"""
    # so hapa if after saving the team retrieve its past played matches run them through the analyser
    # and resave them
    this = Team.query.filter(Team.team_name == team).first()
    if this is None:
        team_obj = Team(team_name=team, logo=logo)
        db.session.add(team_obj)
        db.session.commit()
        return team_obj
    else:
        # we have it already in the database and thus has matches it has played in recorded in matches table
        res = get_team_recent_x(home_team=team, x=10000, overall=True)
        res['home'] = marshmallow(res['home'])
        # res represents the past matches that the team has been involved in, its the input data
        # for our teams analyser
        flag_response = top_team(res['home'])
        this.ov, this.un, this.gg, this.ng = False, False, False, False
        if 'ov' in flag_response:
            this.ov = True
        if 'un' in flag_response:
            this.un = True
        if 'gg' in flag_response:
            this.gg = True
        if 'ng' in flag_response:
            this.ng = True
        db.session.commit()
    return this

def pre_save(diction):
    """Abstracts  common operation to both the save_match and the save_flagged methods"""
    country_obj = save_country(diction['country'])
    if not country_obj:
        country_obj = Country.query.filter(Country.country_name == diction['country']).first()
    league_obj = save_league(diction['country'], diction['league'])
    if not league_obj:
        league_obj = League.query.filter(League.country_name ==
                                         country_obj.country_name).filter(
            League.league_name == diction['league']).first()
    home_team_obj = save_team(diction['home_team'], diction['home_logo_src'])
    away_team_obj = save_team(diction['away_team'], diction['away_logo_src'])

    if not home_team_obj:
        home_team_obj = Team.query.filter(Team.team_name == diction['home_team']).first()
    if not away_team_obj:
        away_team_obj = Team.query.filter(Team.team_name == diction['away_team']).first()
    # maybe we can also link to the leam relation from here
    leam = Leam(league_id=league_obj.league_id, team_name=home_team_obj.team_name)
    leam1 = Leam(league_id=league_obj.league_id, team_name=away_team_obj.team_name)
    db.session.add(leam)
    db.session.add(leam1)
    db.session.commit()
    return country_obj, league_obj, home_team_obj, away_team_obj


def save_match(diction):
    """:parameter: dictionary from scrapped data methods
    :return the match obj or false"""
    # check for a duplicate record
    country_obj, league_obj, home_team_obj, away_team_obj = pre_save(diction)
    try:
        match_obj = Match(team_one=home_team_obj.team_name, team_two=away_team_obj.team_name, date=diction['date'],
                          time=diction['time'], league_id=league_obj.league_id)
        match_obj.team_one_first_half_goals = diction['home_first_half_goals']
        match_obj.team_two_first_half_goals = diction['away_first_half_goals']
        match_obj.team_one_second_half_goals = diction['home_second_half_goals']
        match_obj.team_two_second_half_goals = diction['away_second_half_goals']
        match_obj.team_one_match_goals = diction['home_match_goals']
        match_obj.team_two_match_goals = diction['away_match_goals']
        db.session.add(match_obj)
        db.session.commit()
        return match_obj
    except (IntegrityError, FlushError) as error:
        db.session.rollback()
        return False


def save_flagged(diction, *vars):
    """:parameter dict"""
    country_obj, league_obj, home_team_obj, away_team_obj = pre_save(diction)
    flag_obj = Flagged.query.filter(Flagged.date == diction['date']).filter(Flagged.time == diction['time']).filter(
        Flagged.team_two == away_team_obj.team_name).filter(Flagged.team_one == home_team_obj.team_name).first()
    if flag_obj is None:
        # means that we do not have a record that persists this data in the database
        flag_obj = Flagged(team_one=home_team_obj.team_name, team_two=away_team_obj.team_name, date=diction['date'],
                           time=diction['time'], league_id=league_obj.league_id)
    if not len(vars):
        return
    for arg in vars:
        if not isinstance(arg, str):
            raise ValueError('expected str type for arg but got {} for: {}'.format(type(arg), arg))
        if arg == 'ov':
            flag_obj.over = True
            flag_obj.under = False
        elif arg == 'un':
            flag_obj.under = True
            flag_obj.over = False
        if arg == 'gg':
            flag_obj.gg = True
            flag_obj.ng = False
        elif arg == 'ng':
            flag_obj.ng = True
            flag_obj.gg = False
        if arg == '1':
            flag_obj._1 = True
            flag_obj._x = False
            flag_obj._2 = False
        elif arg == 'x':
            flag_obj._x = True
            flag_obj._2 = False
            flag_obj._1 = False
        elif arg == '2':
            flag_obj._2 = True
            flag_obj._1 = False
            flag_obj._x = False
    db.session.add(flag_obj)
    db.session.commit()
    return flag_obj

def team_name_validator( team_name):
    """raises a Valueerror if givene parameters are not strings"""
    if not isinstance(team_name, str):
        raise ValueError

def get_team_recent_x(home_team=None, away_team=None, x=5, overall=True):
    """extract the past upto x matches that the team has recently participated in"""
    # the matches should have been played within the past 5 years
    date_threshhold = datetime.date.today() - datetime.timedelta(days=(365 * 5))
    home_matches, away_matches = [], []
    if home_team:
        team_name_validator(home_team)
        home_matches = Match.query.filter(Match.team_one == home_team).filter(Match.date > date_threshhold).order_by(
            desc(Match.date)).limit(x).all()
        if overall:
            home_matches = Match.query.filter((Match.team_one == home_team) | (Match.team_two == home_team)).filter(
                Match.date > date_threshhold).order_by(desc(Match.date)).limit(x).all()
    if away_team:
        team_name_validator(away_team)
        away_matches = Match.query.filter(Match.team_two == away_team).filter(
            Match.date > date_threshhold).order_by(desc(Match.date)).limit(x).all()
        if overall:
            away_matches = Match.query.filter((Match.team_one == away_team) | (Match.team_two == away_team)).filter(
                Match.date > date_threshhold).order_by(desc(Match.date)).limit(x).all()
    return {
        'home': home_matches,
        'away': away_matches
    }


def get_teams_mutual(home_team, away_team, respective=False, x=6):
    """returns a dictionary of the recent 6 mutual matches that were played within the past 5 years"""
    team_name_validator(home_team)
    team_name_validator(away_team)
    date_threshhold = datetime.date.today() - datetime.timedelta(days=(365 * 5))
    if respective:
        matches = Match.query.filter((Match.team_one == home_team) & (Match.team_two == away_team)).filter(
            Match.date > date_threshhold).order_by(desc(Match.date)).limit(x).all()
        return {
            'mutual': matches
        }
    matches = Match.query.filter(((Match.team_one == home_team) & (Match.team_two == away_team)) |
                                 ((Match.team_one == away_team) & (Match.team_two == home_team))).filter(
        Match.date > date_threshhold).order_by(desc(Match.date)).limit(x).all()
    return {'mutual': matches}

def explain(obj, view=False):
    if isinstance(obj, Match):
        _date = obj.date
        _time = obj.time
        if view:
            _date = _date.strftime('%Y-%m-%d')
            _time = _time.strftime('%H:%M')
        return {
            "home_team": obj.team_one,
            "date": _date,
            "time": _time,
            "league": obj.league_id,
            "away_first_half_goals": obj.team_two_first_half_goals,
            "away_match_goals": obj.team_two_match_goals,
            "home_first_half_goals": obj.team_one_first_half_goals,
            "away_team": obj.team_two,
            "home_match_goals": obj.team_one_match_goals,
            "away_second_half_goals": obj.team_two_second_half_goals,
            "home_second_half_goals": obj.team_one_second_half_goals
        }
    elif isinstance(obj, Flagged):
        return{
            "home_team": obj.team_one,
            "date": obj.date.strftime('%Y-%m-%d'),
            "time": obj.time.strftime('%H:%M'),
            "away_team": obj.team_two
        }

    elif isinstance(obj, Team):
        return {
            "team_name": obj.team_name,
            "logo": obj.logo
        }
    else:
        raise TypeError('only Match and Team objects can be explained into dicts, got {}'.format(type(obj)))

def marshmallow(match_list):
    """we need to create our function that serializes our match objects from the database to match our scrap
    format from the website"""
    result_list = []
    for match in match_list:
        result_list.append(explain(match))
    return result_list


def get_matches(model, date_obj, over=False, under=False, gg=False, ng=False):
    partial_res = model.query.join(League, model.league_id == League.league_id).\
        join(Country, Country.country_name == League.country_name).\
        with_entities(League.league_name, model, Country.country_name).\
        filter(model.date == date_obj)
    result_list = []
    if model == Flagged:
        if over:
            res = partial_res.filter(model.over == True).all()
        if under:
            res = partial_res.filter(model.under == True).all()
        if gg:
            res = partial_res.filter(model.gg == True).all()
        if ng:
            res = partial_res.filter(model.ng == True).all()
    else:
        res = partial_res.all()
    for collection in res:
        match_dict = explain(collection[1], view=True)
        match_dict["country"] = collection[2]
        match_dict["league"] = collection[0]
        result_list.append(match_dict)
    return result_list

def get_teams(over=False, under=False, gg=False, ng=False):
    res = Team.query
    if over:
        return list(map(explain, res.filter(Team.over == True).all()))
    elif under:
        return list(map(explain, res.filter(Team.under == True).all()))
    elif gg:
        return list(map(explain, res.filter(Team.ng == True).all()))
    elif ng:
        return list(map(explain, res.filter(Team.ng == True).all()))