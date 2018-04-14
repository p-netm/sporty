"""My little ai"""
# get match details: i.e the home team and away team
from .scrapper import scrap_all_links, get_specific_match_details, retrieve_mutual_matches_data, BeautifulSoup
from .tango import get_team_recent_x, get_teams_mutual, save_flagged, marshmallow

def starter():
    match_list = scrap_all_links()
    for each_tuple in match_list:
        home_team = each_tuple[0]
        away_team = each_tuple[1]
        # we can get the team's country and league from the url
        url = each_tuple[2]
        recent = get_team_recent_x(home_team=home_team, away_team=away_team)
        recent['home'] = marshmallow(recent['home'])
        recent['away'] = marshmallow(recent['away'])
        mutual = marshmallow(get_teams_mutual(home_team, away_team)['mutual'])
        soup = BeautifulSoup(url, 'html.parser')
        match_data = get_specific_match_details(soup)
        if len(mutual) < 6:
            # we proceed with our scrap functions
            mutual = retrieve_mutual_matches_data(soup)['mutual']
        # we can now run the respective evaluators on the return data
        data = {}
        data.update(recent)
        data.update(mutual)
        # we run the database persistence functions for each data point
        _vars = []
        if ov(data):
            _vars.append('ov')
        if un(data):
            _vars.append('un')
        if gg(data):
            _vars.append('gg')
        if ng(data):
            _vars.append('ng')
        save_flagged(match_data, _vars)


def ov(diction, market='ov'):
    """:parameters: a diction representing home teams recent x matches
    a dict representing the away teams recent x matches
    a dict representing the mutual matches
    :returns boolean
    """
    return mini_evaluator(diction, market)

def recent_evaluator(match_list, index, frac, market):
    if len(match_list) > 4:
        for match in match_list:
            if market == 'un' and sum(match['home_match_goals'], match['away_match_goals']) < 2.5:
                index += 1
            elif market == 'ov' and sum(match['home_match_goals'], match['away_match_goals']) > 2.5:
                index += 1
        frac = index / len(match_list)
    return index, frac

def un(diction, market='un'):
    """:parameters: a diction representing home teams reent x matches
    a dict representing the away teams recent x matches
    a dict representing the mutual matches
    :returns boolean"""
    return mini_evaluator(diction, market)

def recent_evaluator_for_g(match_list, index, frac, market):
    if len(match_list) > 4:
        for match in match_list:
            if market == 'gg' and match['home_match_goals'] and match['away_match_goals']:
                index += 1
            elif market == 'ng' and not match['home_match_goals'] and match['away_match_goals']:
                index += 1
        frac = index / len(match_list)
    return index, frac

def mini_evaluator(diction, market):
    home_index, away_index, mutual_index, mutual_goals_index = 0, 0, 0, 0
    home_frac, away_frac, mutual_frac, mutual_goals_frac = 1, 1, 1, 1
    home_index, home_frac = recent_evaluator(diction['home'], home_index, home_frac, market)
    away_index, away_frac = recent_evaluator(diction['away'], away_index, away_frac, market)
    mutual_index, mutual_frac = recent_evaluator(diction['mutual'], mutual_index, mutual_frac, market)
    full_index = 0
    if market != 'gg' or market != 'ng':
        mutual_goals_index = sum(
            [sum(match['home_match_goals'], match['away_match_goals']) for match in diction['mutual']])
        no_ = len([sum(match['home_match_goals'], match['away_match_goals']) for match in diction['mutual']])
        mutual_goals_frac = mutual_goals_index / no_
    if market == 'un':
        mutual_goals_frac = (3 * no_ - mutual_goals_index) / no_
    if market != 'gg' or market != 'ng':
        full_index = (home_frac * 5) / 5 * (away_frac * 5) / 5 * (mutual_frac * 6) / 6 * ((mutual_goals_frac * 6) / 6) / 2.5
        threshhold = 0.3675
    if market == 'gg' or market == 'ng':
        full_index = (home_frac * 5) / 5 * (away_frac * 5) / 5 * (mutual_frac * 6) / 6
        threshhold = 0.48
    if full_index > threshhold:
        return True
    else:
        return False

def gg(diction):
    """:parameters: a diction representing home teams recent x matches
    a dict representing the away teams recent x matches
    a dict representing the mutual matches
    :returns boolean"""
    return mini_evaluator(diction, market='gg')


def ng(diction):
    """:parameters: a diction representing home teams recent x matches
    a dict representing the away teams recent x matches
    a dict representing the mutual matches
    :returns boolean"""
    return mini_evaluator(diction, market='ng')
