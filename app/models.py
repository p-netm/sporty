<<<<<<< HEAD
from . import db


=======
"""Definition of all the class models that wil be mapped onto a daabase
unlike for the eanmble ts, te eanmble sp will be a bit different due the increased level of operations and 
data manipulations involved in getting to a reasonable fixture prediction analysis
"""
from . import db

<<<<<<< HEAD
>>>>>>> 106c6f1de13e7616203fcad48f5c8f779fe02b43
=======

>>>>>>> scrapper
class Team(db.Model):
    """Represents the data that will be saved about a specific team

    a representation of the aspects that are most important in this preliminary
    survey, this aspects will be added to the data csv file
    """
<<<<<<< HEAD
<<<<<<< HEAD
    __tablename__ = 'Teams'
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100))
    date_founded = db.Column(db.DATE, nullable=True)
    logo = db.Column(db.TEXT, nullable=True)
    nick_name = db.Column(db.String(100), nullable=True)
    short_name = db.Column(db.String(30), nullable=True)
    website = db.Column(db.String(500), nullable=True)
    kits = db.Column(db.String(500), nullable=True)

    # id = Column(Integer, primary_key=True)
    # time = Column(Integer)
    # team_name = Column(String)
    # country = Column(String)
    # league = Column(String)
    # goals_conceded = Column(Integer)
    # goals_scored = Column(Integer)
    # logo = Column(String)
    # flagged = Column(Integer, default=0)
    # # types of checkers that we will be using: over, under, win, loss, draw,
    # ou_25 = Column(Boolean)
    # result = Column(Enum('1', 'x', '2'))


    def __init__(self, team_name, time, country_name, league_name, goals_scored, goals_conceded, logo):

        if type(country_name) is not str:
            raise TypeError('The Country_Name')
        self.country = country_name

        if not isinstance(team_name, str):
            raise TypeError('The Team_name is not a String')
        self.team_name = team_name

        if not isinstance(league_name, str):
            raise TypeError('unrecognized format for league name')
        self.league = league_name

        if not isinstance(logo, str):
            raise TypeError('Logo is not of a valid type')
        self.logo = logo

        if not isinstance(goals_conceded, int) or not isinstance(goals_scored, int):
            raise TypeError('Unrecognized format for both goals scored and goals conceded')
        self.goals_conceded = goals_conceded
        self.goals_scored = goals_scored

        self.time = time

    def __repr__(self):
        """formats a string into an arbitrary string presentation"""
        return '<{}{}{}{}{}{}{}>'.format(self.id, self.team_name, self.time, self.country,
                                self.league, self.goals_scored, self.goals_conceded)

    # class Continent(db.Model):
    #     __tablename__ = 'Continents'
    #
    #     continent_name = db.Column(db.String(45), primary_key=True)
    #     color_code = db.Column(db.String(10), unique=True)
    #     size = db.Column(db.Integer)
    #     population = db.Column(db.Integer)
    #
    #     def __init__(self, continent_name, color_code, size, population):
    #         self.continent_name = continent_name
    #         self.color_code = color_code
    #         self.size = size
    #         self.population = population


    class Country(db.Model):
        __tablename__ = 'Countries'

        country_code = db.Column(db.String(10), primary_key=True)
        country_name = db.Column(db.String(150), unique=True)
        color_code = db.Column(db.String(10))
        size = db.Column(db.Integer)
        population = db.Column(db.Integer)
        # currency = db.Column(db.String(30))
        # coat_of_arms = db.Column(db.String())
        flag_picture = db.Column(db.String(100))
        # gdp = db.Column(db.DECIMAL(10,2))
        # continent_name  = db.Column(db.String(45), db.ForeignKey('Continents.continent_name'))
        #
        # continent = db.relationship('Continent', back_populates='Countries')

        def __init__(self, country_code, country_name, continent_name):
            self.country_code = country_code
            self.country_name = country_name
            self.continent_name = continent_name


    # class Team(db.Model):
    #     __tablename__ = 'Teams'
    #
    #
    #     # league_id = db.Column(db.String(10))
    #     # manager_name = db.Column(db.String(45))


    class Match(db.Model):
        __tablename__ = 'Matches'

        match_id = db.Column(db.String(20), primary_key=True)
        date = db.Column(db.DATE, nullable=False)
        time = db.Column(db.TIME, nullable=False)
        team1 = db.Column(db.Integer, db.ForeignKey('Teams.team_id'))
        team2 = db.Column(db.Integer, db.ForeignKey('Teams.team_id'))
        # refa = db.Column(db.String(100))
        # season = db.Column(db.String(10))
        # averaged_match_odds = db.Column(DECIMAL, db.ForeignKey(''))
        results_id = db.Column(db.String(10), db.ForeignKey('Results.result_id'))
        # stadium_name = db.Column(db.String(150), db.ForeignKey('Stadiums.stadium_name'), nullable=True)

    class League(db.Model):
        __tablename__ = 'leagues'

        league_id = db.Column(db.String(20), primary_key=True)


    # class Result(db.Model):
    #     __tablename__ = "Results"
    #
    #     result_id = db.Column(db.String(10), primary_key=True)
    #     full_time_home_goals = db.Column(db.Integer)
    #     full_time_away_goals = db.Column(db.Integer)
    #     half_time_home_goals = db.Column(db.Integer)
    #     half_time_away_goals = db.Column(db.Integer)

    # class Stadium(db.Model):
    #     __tablename__ = 'Stadiums'
    #
    #     stadium_name = db.Column(db.String(100), primary_key=True)
    #     stadium_code = db.Column(db.Integer)
    #     capacity = db.Column(db.String())
    #     country_code = db.Column(db.String(10), db.ForeignKey('Countries.country_code'))
    #     team_id = db.Column(db.Integer, db.ForeignKey('Teams.team_id'))

        # country = db.relationship('Country', back_populates='Stadiums')

    # class Prediction(db.Model):
    #     __tablename__ = 'Predictions'
    #
    #     prediction_id = db.Column(db.Integer, primary_key=True)
    #     probability = db.Column(db.Integer)
    #     match_id = db.Column(db.String(20), db.ForeignKey('Matches.match_id'))
    #     bet_id = db.Column(db.String(10), db.ForeignKey('Bets.bet_id'))
=======

    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String())
    league_id = db.Column(db.Integer, db.ForeignKey('league.league_id'), nullable=False)
    logo = db.Column(db.String())
=======
    team_name = db.Column(db.String(), unique=True, primary_key=True)
    logo = db.Column(db.String(), nullable=True)  # can set unique to true
>>>>>>> scrapper
    # the below flag attributes are for top-teams section
    over = db.Column(db.Boolean(), nullable=False, default=False)
    gg = db.Column(db.Boolean(), nullable=False, default=False)
    ng = db.Column(db.Boolean(), nullable=False, default=False)
    under = db.Column(db.Boolean(), nullable=False, default=False)
    win = db.Column(db.Boolean(), nullable=False, default=False)
    draw = db.Column(db.Boolean(), nullable=False, default=False)
    loss = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self):
        """formats a string into an arbitrary string presentation"""
        return '<Team {}>'.format(self.team_name)
    
    
class Country(db.Model):
    """
    One country holds or rather has several leagues
    a one to many relationship to that of the league models
    """
    country_name = db.Column(db.String(), primary_key=True)
    flag_icon = db.Column(db.String, nullable=True)
    leagues = db.relationship('League', backref='country', lazy=True)
    
    def __repr__(self):
        """string serialisation"""
        return '< Country {}>'.format(self.country_name)
    

class League(db.Model):
    """
    relation: one country holds several leagues
    one league holds several teams
    """
    league_id = db.Column(db.Integer, primary_key=True)
    league_name = db.Column(db.String())
    country_name = db.Column(db.String(), db.ForeignKey('country.country_name'), nullable=False)

    __table_args__ = (db.UniqueConstraint('league_name', 'country_name', name='country_league_cons'), {})

    def __repr__(self):
        """string serialisation"""
        return '<League {} {}>'.format(self.league_id, self.league_name)


class Leam(db.Model):
    """A many to many relation between the leagues and teams
    one team may play in several leagues -> i know this is stupid logic
    and definitely one league has several teams
    """
    leam_id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, db.ForeignKey('league.league_id'), nullable=False)
    team_name = db.Column(db.String(), db.ForeignKey('team.team_name'), nullable=False)

    def __repr__(self):
        """Meaningless"""
        return '<Leam {} {}>'.format(self.league_id, self.team_name)

    
class Match(db.Model):
    """:relation: one match will involves two teams"""
    match_id = db.Column(db.Integer, primary_key=True)
    team_one = db.Column(db.String(), db.ForeignKey('team.team_name'), nullable=False)
    team_two = db.Column(db.String(), db.ForeignKey('team.team_name'), nullable=False)
    league_id = db.Column(db.Integer, db.ForeignKey('league.league_id'), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    time = db.Column(db.Time(), nullable=False)
    team_one_first_half_goals = db.Column(db.Integer, nullable=True)
    team_two_first_half_goals =db.Column(db.Integer, nullable=True)
    team_one_second_half_goals = db.Column(db.Integer, nullable=True)
    team_two_second_half_goals = db.Column(db.Integer, nullable=True)
    team_one_match_goals = db.Column(db.Integer, nullable=True)
    team_two_match_goals = db.Column(db.Integer, nullable=True)

    __table_args__= (db.UniqueConstraint('date', 'team_one', 'team_two', name='date_teams_cons'),)
    
    def __repr__(self):
        """ This is pretty basic """
        return '<Match {} {} {} {} {} {} {}>'.format(self.match_id, self.team_one, self.team_two, self.date, self.time,
                                           self.team_one_match_goals, self.team_two_match_goals)
    
    
class Flagged(db.Model):
    """:relation just as that of a match, involves two matches"""
    flag_id = db.Column(db.Integer, primary_key=True)
    team_one = db.Column(db.String(), db.ForeignKey('team.team_name'), nullable=False)
    team_two = db.Column(db.String(), db.ForeignKey('team.team_name'), nullable=False)
    league_id = db.Column(db.Integer, db.ForeignKey('league.league_id'), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    time = db.Column(db.Time(), nullable=False)
    over = db.Column(db.Boolean(), nullable=False, default=False)
    gg = db.Column(db.Boolean(), nullable=False, default=False)
    ng = db.Column(db.Boolean(), nullable=False, default=False)
    under = db.Column(db.Boolean(), nullable=False, default=False)
    _1 = db.Column(db.Boolean(), nullable=False, default=False)
    _x = db.Column(db.Boolean(), nullable=False, default=False)
    _2 = db.Column(db.Boolean(), nullable=False, default=False)

    
    def __repr__(self):
        """This is pretty basic"""
<<<<<<< HEAD
        return '<{} {} {} {} {}>'.format(self.flag_id, self.team_one, self.team_two, self.date, self.time)
    
>>>>>>> 106c6f1de13e7616203fcad48f5c8f779fe02b43
=======
        return '<{} {} {} {} {} 1.{} x.{} 2.{}>'.format(self.flag_id, self.team_one, self.team_two, self.date, self.time,
                                                        self._1, self._x, self._2)

class SubscribedEmail(db.Model):
    email = db.Column(db.String(), primary_key=True)
    
    def __repr__(self):
        return '<email {}>'.format(self.email)
    
>>>>>>> scrapper
