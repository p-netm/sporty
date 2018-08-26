"""My little ai"""
# get match details: i.e the home team and away team


def ov(diction, market='ov'):
    """:parameters: a diction representing home teams recent x matches
    a dict representing the away teams recent x matches
    a dict representing the mutual matches
    :returns boolean
    """
    return mini_evaluator(diction, market)

def recent_evaluator(match_list, market):
    index, frac = 0, 1
    if len(match_list) > 4:
        for match in match_list:
            if market == 'un' and sum([match['home_match_goals'], match['away_match_goals']]) < 2.5:
                index += 1
            elif market == 'ov' and sum([match['home_match_goals'], match['away_match_goals']]) > 2.5:
                index += 1
            elif market == 'gg' and match['home_match_goals'] and match['away_match_goals']:
                index += 1
            elif market == 'ng' and ((not match['home_match_goals'] and match['away_match_goals']) or
                                     (match['home_match_goals'] and not match['away_match_goals'])):
                index += 1
        frac = index / len(match_list)
    return index, frac


def un(diction, market='un'):
    """:parameters: a diction representing home teams reent x matches
    a dict representing the away teams recent x matches
    a dict representing the mutual matches
    :returns boolean"""
    return mini_evaluator(diction, market)


def mini_evaluator(diction, market):
    """
    we use an index to track the quantifiable aspect of a certain market precedence that we are tracking
    the frac part is the fraction(ratio) of the index to an expected whole
    """
    home_index, away_index, mutual_index, mutual_goals_index = 0, 0, 0, 0
    home_frac, away_frac, mutual_frac, mutual_goals_frac = 1, 1, 1, 1
    home_index, home_frac = recent_evaluator(diction['home'], market)
    away_index, away_frac = recent_evaluator(diction['away'], market)
    mutual_index, mutual_frac = recent_evaluator(diction['mutual'], market)
    full_index = 0
    if market != 'gg' and market != 'ng':
        mutual_goals_index = sum(
            [sum([match['home_match_goals'], match['away_match_goals']]) for match in diction['mutual']])
        no_ = len([sum([match['home_match_goals'], match['away_match_goals']]) for match in diction['mutual']])
        mutual_goals_frac = mutual_goals_index / no_
        if market == 'un':
            mutual_goals_frac = (3 * no_ - mutual_goals_index) / no_
    if market  == 'ov' or market == 'un':
        full_index = (home_frac * 5) / 5 * (away_frac * 5) / 5 * (mutual_frac * 6) / 6 * ((mutual_goals_frac * 6) / 6) / 2.5
        threshhold = 0.3675
        if market == 'un':
            threshhold = 0.147
    if market == 'gg' or market == 'ng':
        full_index = (home_frac * 5) / 5 * (away_frac * 5) / 5 * (mutual_frac * 6) / 6
        threshhold = 0.48
    print('\n', market, full_index, '\n')  # only for debugging
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

"""Analyser functions for specific matches for the Top Team in a certain market classification"""
def top_team(diction):
    markets = ['ov', 'un', 'gg', 'ng']
    results = []
    for mark in markets:
        index, frac = recent_evaluator(diction, mark)
        if frac > 0.7:
            results.append(mark)
    return results
