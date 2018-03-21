"""
Tango is where operation controls happen, defined here, you will find
methods ready to initialise the scrap engine, save the data in our trusty
databases and then invoke the evalator on the saved data 
"""
from ..models import *
from .scrapper import _run_
from sqlalchemy.exc import IntegrityError


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
    makes sure we do not have redundant info being added  to our databases"""
    # counries have unique names
    # leagues may ahve similar names but not in the same country
    # teams may have similar names but not in the same league(i hope)
    return save_match(diction)


def save_country(country):
    """:paramter: a string variable of the country name to be saved
    :returns: True at successful completion of the operation, otherwise will return False
    if the country is already existent
    """
    try:
        country_obj = Country(counntry_name=country)
        db.session.add(country_obj)
        db.session.commit()
        return country_obj
    except IntegrityError as e:
        db.session.rollback()
        return False


def save_league(country, league):
    """:prameters: the country_name and the league name
    :returns: True if the league is succesfully added and linked to a country
    false if the league already exists
    """
    country_obj = Country.query.filter_by(country_name=country).first()  # returns a single object
    if country_obj is None:
        country_obj = save_country(country)

    # query if the league exists and add it if it does not
    leagues = League.filter(League.country_id == country_obj.country.id).filter(League.league_name == league).first()
    if leagues is None:
        # greenlight
        league_obj = League(league_name=league, country_id=country_obj.id)
        db.session.add(league_obj)
        db.session.commit()
        return league_obj
    return False


def save_team(country, league, team, logo):
    """:prameters: the country_name, league_name, and the team_name, all as string
    :returns Boolean if operation successful otherwise false if team already existent"""
    league_obj = League.query.filter_by(league_name=league).first()
    if league_obj is None:
        league_obj = save_league(country, league)
    teams = Team.filter(Team.league_id == league_obj.id).filter(Team.team_name == team).first()
    if teams is None:
        team_obj = Team(team_name=team, league_id=league_obj.id, logo=logo)
        db.session.add(team_obj)
        db.session.commit()
        return team_obj
    return False


def pre_save(diction):
    """Abstacts  common operation to both the save_match and the save_flagged methods"""
    country_obj = save_country(diction['country'])
    if not country_obj:
        country_obj = Country.query.filter(Country.country_name == diction['country']).first()
    league_obj = save_league(diction['country'], diction['league'])
    if not league_obj:
        league_obj = League.filter(League.country_id ==
                                   country_obj.country.id).filter(League.league_name == diction['league']).first()
    home_team_obj = save_team(diction['coutry'], diction['league'], diction['home_team'], diction['home_logo_src'])
    away_team_obj = save_team(diction['coutry'], diction['league'], diction['away_team'], diction['away_logo_src'])
    if not home_team_obj:
        home_team_obj = Team.filter(Team.league_id == league_obj.id).filter(
            Team.team_name == diction['home_team']).first()
    if not away_team_obj:
        away_team_obj = Team.filter(Team.league_id == league_obj.id).filter(
            Team.team_name == diction['away_team']).first()
    return country_obj, league_obj, home_team_obj, away_team_obj


def save_match(diction):
    """:parameter: dictionary from scrapped data methods
    :return the match obj or false"""
    # check for a duplicate record
    country_obj, league_obj, home_team_obj, away_team_obj = pre_save(diction)
    dup = Match.query.filter(Match.date == diction['date']).filter(Match.time == diction['time']).filter(
        Match.team_two == away_team_obj.id).filter(Match.team_one == home_team_obj.id).first()
    if dup is None:
        # green light
        match_obj = Match(team_one=home_team_obj.id, team_two=away_team_obj.id, date=diction['date'],
                          time=diction['time'])
        match_obj.team_one_first_half_goals = diction['home_first_half_goals']
        match_obj.team_two_first_half_goals = diction['away_first_half_goals']
        match_obj.team_one_second_half_goals = diction['home_second_half_goals']
        match_obj.team_two_second_half_goals = diction['away_second_half_goals']
        match_obj.team_one_match_goals = diction['home_match_goals']
        match_obj.team_two_match_gaols = diction['away_match_goals']
        db.session.add(match_obj)
        db.session.commit()
        return match_obj
    return False


def save_flagged(diction, *vars):
    """:parameter dict"""
    country_obj, league_obj, home_team_obj, away_team_obj = pre_save(diction)
    flag_obj = Flagged.query.filter(Match.date == diction['date']).filter(Match.time == diction['time']).filter(
        Match.team_two == away_team_obj.id).filter(Match.team_one == home_team_obj.id).first()
    if flag_obj is None:
        flag_obj = Flagged(team_one=home_team_obj.id, team_two=away_team_obj.id, date=diction['date'],
                           time=diction['time'])
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

def retriever():
    """"""
    pass


def get_team_recent_x(country_name, league_name, home_team=None, away_team=None, x=5, overall=False):
    """extract the past upto x matches that the team has recently participated in"""
    # the matches should have been played within the past 6 years
    country = Country.query.filter_by(country_name=country_name).first()
    wanted_league = None
    for league in country.leagues:
        if league.league_name == league_name:
            wanted_league = league
            break

    for team in wanted_league.teams:
        if team.team_name == home_team:
            home_team = team
        if team.team_name == away_team:
            away_team = team

    home_matches, away_matches = [], []
    if home_team:
        home_matches = Match.query.filter(Match.team_one == home_team.team_id).all()
        if overall:
            home_matches = Match.query.filter((Match.team_one == home_team.team_id) | (Match.team_two == home_team.team_id))
    if away_team:
        away_matches = Match.query.filter(Match.team_two == away_team.team_id).all()
        if overall:
            away_matches = Match.query.filter((Match.team_one == away_team.team_id) | (Match.team_two == away_team.team_id))
    return {
        'home': home_matches,
        'away': away_matches
        }


def get_teams_mutual(home_team, away_team, league_name, respective=False):
    """returns a dictionary of the recent 6 mutual matches that were played within the past 5 years"""
    league = League.query.filter_by(league_name=league_name).first()
    for team in league.teams:
        if team.team_name == home_team:
            home = team
        if team.team_name == away_team:
            away = team
    if respective:
        matches = Match.query.filter((Match.team_one == home.team_id) & (Match.team_two == away.team_id))
        return {
            'mutual': matches
        }
    matches = Match.query.filter(((Match.team_one == home.team_id) & (Match.team_two == away.team_id)) | ((Match.team_one == away.team_id) & (Match.team_two == home.team_id))).all()
    return matches
