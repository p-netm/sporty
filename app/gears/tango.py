"""
Tango is where operation controls happen, defined here, you will find
methods ready to initialise the scrap engine, save the data in our trusty
databases and then invoke the evalator on the saved data 
"""

def saver(url=None):
	"""Officer in charge of defensive operations, commands the scrap functions
	to go and get data, in other words you could say he is in charge of reconnaisance
	:parameters: specific url to scrap from, the urls only defer in date
	:returns: boolean value or flags an error if it runs into one"""
	pass


def saver_worker(diction):
	"""saver subcommandant incharge of data verification and the actual work of saving.
	makes sure we do not have redundant info being added  to our databases"""
	# counries have unique names 
	# leagues may ahve similar names but not in the same country
	# teams may have similar names but not in the same league(i hope)
	pass

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
	country_obj = Country.query.filter_by(country_name=country).first() # returns a single object
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

def save_match(diction, flagged=False, *vars):
	""":parameter: dictionary from scrapped data methods
	:return the match obj or false"""
	country_obj = save_country(diction['country'])
	if not country_obj:
		country_obj = Country.query.filter(Country.country_name == diction['country']).first()
	league_obj = save_league(diction['country'], diction['league'])
	if not league_obj:
		league_obj = League.filter(League.country_id ==
								   country_obj.country.id).filter(League.league_name == league).first()
	home_team_obj = save_team(diction['coutry'], diction['league'], diction['home_team'], diction['home_logo_src'])
	away_team_obj = save_team(diction['coutry'], diction['league'], diction['away_team'], diction['away_logo_src'])
	if not home_team_obj:
		home_team_obj = Team.filter(Team.league_id == league_obj.id).filter(Team.team_name == diction['home_team']).first()
	if not away_team_obj:
		away_team_obj = Team.filter(Team.league_id == league_obj.id).filter(Team.team_name == diction['away_team']).first()
	# check for a duplicate record
	if not flagged:
		dup = Match.query.filter(Match.date == diction['date']).filter(Match.time == diction['time']).filter(Match.team_two == away_team_obj.id).filter(Match.team_one == home_team_obj.id).first()
		if dup is None:
			# green light
			match_obj = Match(team_one=home_team_obj.id, team_two=away_team_obj.id, date=diction['date'], time=diction['time'])
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
	dup = Flagged.query.filter(Match.date == diction['date']).filter(Match.time == diction['time']).filter(Match.team_two == away_team_obj.id).filter(Match.team_one == home_team_obj.id).first()
	if dup is None:
		flag_obj = Flagged(team_one=home_team_obj.id, team_two=away_team_obj.id, date=diction['date'], time=diction['time'])
		# the flag market classification
		if not len(vars):
			return
		for arg in vars:
			if not isinstance(arg, str):
				raise ValueError('expected str type for arg but got {} for: {}'.format(type(arg), arg))
			if arg == 'ov':
				flag_obj.over = True
			elif: arg == 'un':
				flag_obj.under = True
			if arg == 'gg':
				flag_obj.gg = True
			elif arg == 'ng':
				flag_obj.ng = True
			if arg == '1':
				flag_obj._1 = True
			elif arg == 'x':
				flag_obj._x = True
			elif arg == '2':
				flag_obj._2 = True
		db.session.add(flag_obj)
		db.session.commit()
		return flag_obj
	return False

def save_flagged(diction, *vars):
	""":parameter dict"""
	return save_match(diction, flagged=True, *vars)

def evaluator():
	"""evaluates and decides what teams gets flagged in which classification is it placed"""
	pass
	