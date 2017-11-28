from . import db


class Team(db.Model):
    """Represents the data that will be saved about a specific team

    a representation of the aspects that are most important in this preliminary
    survey, this aspects will be added to the data csv file
    """
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

    class Continent(db.Model):
        __tablename__ = 'Continents'

        continent_name = db.Column(db.String(45), primary_key=True)
        color_code = db.Column(db.String(10), unique=True)
        size = db.Column(db.Integer)
        population = db.Column(db.Integer)

        def __init__(self, continent_name, color_code, size, population):
            self.continent_name = continent_name
            self.color_code = color_code
            self.size = size
            self.population = population


    class Country(db.Model):
        __tablename__ = 'Countries'

        country_code = db.Column(db.String(10), primary_key=True)
        country_name = db.Column(db.String(150), unique=True)
        color_code = db.Column(db.String(10))
        size = db.Column(db.Integer)
        population = db.Column(db.Integer)
        currency = db.Column(db.String(30))
        coat_of_arms = db.Column(db.String())
        flag_picture = db.Column(db.String(100))
        gdp = db.Column(db.DECIMAL(10,2))
        continent_name  = db.Column(db.String(45), db.ForeignKey('Continents.continent_name'))

        continent = db.relationship('Continent', back_populates='Countries')

        def __init__(self, country_code, country_name, continent_name):
            self.country_code = country_code
            self.country_name = country_name
            self.continent_name = continent_name


    class Team(db.Model):
        __tablename__ = 'Teams'


        # league_id = db.Column(db.String(10))
        # manager_name = db.Column(db.String(45))


    class Match(db.Model):
        __tablename__ = 'Matches'

        match_id = db.Column(db.String(20), primary_key=True)
        date = db.Column(db.DATE, nullable=False)
        time = db.Column(db.TIME, nullable=False)
        team1 = db.Column(db.Integer, db.ForeignKey('Teams.team_id'))
        team2 = db.Column(db.Integer, db.ForeignKey('Teams.team_id'))
        refa = db.Column(db.String(100))
        season = db.Column(db.String(10))
        # averaged_match_odds = db.Column(DECIMAL, db.ForeignKey(''))
        results_id = db.Column(db.String(10), db.ForeignKey('Results.result_id'))
        stadium_name = db.Column(db.String(150), db.ForeignKey('Stadiums.stadium_name'), nullable=True)


    class Result(db.Model):
        __tablename__ = "Results"

        result_id = db.Column(db.String(10), primary_key=True)
        full_time_home_goals = db.Column(db.Integer)
        full_time_away_goals = db.Column(db.Integer)
        half_time_home_goals = db.Column(db.Integer)
        half_time_away_goals = db.Column(db.Integer)

    class Stadium(db.Model):
        __tablename__ = 'Stadiums'

        stadium_name = db.Column(db.String(100), primary_key=True)
        stadium_code = db.Column(db.Integer)
        capacity = db.Column(db.String())
        country_code = db.Column(db.String(10), db.ForeignKey('Countries.country_code'))
        team_id = db.Column(db.Integer, db.ForeignKey('Teams.team_id'))

        country = db.relationship('Country', back_populates='Stadiums')

    class Prediction(db.Model):
        __tablename__ = 'Predictions'

        prediction_id = db.Column(db.Integer, primary_key=True)
        probability = db.Column(db.Integer)
        match_id = db.Column(db.String(20), db.ForeignKey('Matches.match_id'))
        bet_id = db.Column(db.String(10), db.ForeignKey('Bets.bet_id'))


    class Bet(db.Model):
        __tablename__ = 'Bets'

        bet_id = db.Column(db.String(20), primary_key=True)
        bet_name = db.Column(db.String(200))
        bet_description = db.Column(db.String(500))
        average_odds = db.Column(db.DECIMAL(4,2))