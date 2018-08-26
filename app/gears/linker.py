from .scrapper import scrap_all_links, get_specific_match_details, retrieve_mutual_matches_data, BeautifulSoup
from .tango import get_team_recent_x, get_teams_mutual, save_flagged, marshmallow
from .analyser import ov, un, gg, ng

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
