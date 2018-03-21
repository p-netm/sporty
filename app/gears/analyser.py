"""My little ai"""
# get match details: i.e the home team and away team
from .scrapper import scrap_all_links, get_specific_match_details, retrieve_mutual_matches_data
from .tango import get_recent_x, get_teams_mutual
match_list = scrapp_all_links()
for each_tuple in match_list:
	home_team = each_tuple[0]
	away_team = each_tuple[1]
	# we can get the team's country and league from the url
	url = each_tuple[2]
	country = url.split('/')[4]
	league = url.split('/')[5]
	recent = get_recent_x(country, league, home_team=home_team, away_team=away_team)
	home_recent = recent['home']
	away_recent = recent['away']
	mutual = get_teams_mutual(league, home_team, away_team)['mutual']
	if len(mutual) < 6:
		# we proceed with our scrap functions
		soup = BeautifulSoup(url, 'html.parser')
		mutual = retrieve_mutual_matches_data(soup)['mutual']
		# we can now run the respective evaluators on the return data
		

def ov():
	""":parameters: a diction representing home teams reent x matches
	a dict repreenting the away teams recent x matches
	a dict representing the mutual matches
	:returns boolean"""
	pass

def un():
	""":parameters: a diction representing home teams reent x matches
	a dict repreenting the away teams recent x matches
	a dict representing the mutual matches
	:returns boolean"""
	pass
	
def gg():
	""":parameters: a diction representing home teams reent x matches
	a dict repreenting the away teams recent x matches
	a dict representing the mutual matches
	:returns boolean"""
	pass

def ng():
	""":parameters: a diction representing home teams reent x matches
	a dict repreenting the away teams recent x matches
	a dict representing the mutual matches
	:returns boolean"""
	pass
	
def streak