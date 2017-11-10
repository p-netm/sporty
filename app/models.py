"""Definition of all the class models that wil be mapped onto a daabase
unlike for the eanmble ts, te eanmble sp will be a bit different due the increased level of operations and 
data manipulations involved in getting to a reasonable fixture prediction analysis
"""
from . import db

class Team(db.Model):
    """Represents the data that will be saved about a specific team

    a representation of the aspects that are most important in this preliminary
    survey, this aspects will be added to the data csv file
    """
    __tablename__ = 'Teams'

    id = db.Column(db.Integer(), primary_key=True)
    date_time = db.Column(db.DateTime())
    team_name = db.Column(db.String())
    country = db.Column(db.String())
    league = db.Column(db.String())
    goals_conceded = db.Column(db.Integer())
    goals_scored = db.Column(db.Integer())
    logo = db.Column(db.String())
    flagged = db.Column(db.Integer(), default=0)
    # types of checkers that we will be using: over, under, win, loss, draw,
    over = db.Column(db.Boolean())
    under = db.Column(db.Boolean())
    win = db.Column(db.Boolean())
    draw = db.Column(db.Boolean())
    loss = db.Column(db.Boolean())


    def __init__(self, team_name, time, country_name, league_name, goals_scored, goals_conceded):

        if type(country_name) is not str:
            raise TypeError('The Country_Name')
        self.country = country_name

        if not isinstance(team_name, str):
            raise TypeError('The Team_name is not a String')
        self.team_name = team_name

        if not isinstance(league_name, str):
            raise TypeError('unrecognized format for league name')
        self.league = league_name

        if not isinstance(goals_conceded, int) or not isinstance(goals_scored, int):
            raise TypeError('Unrecognized format for both goals scored and goals conceded')
        self.goals_conceded = goals_conceded
        self.goals_scored = goals_scored

        self.time = time

    def __repr__(self):
        """formats a string into an arbitrary string presentation"""
        return 'Team <{}{}{}{}{}{}{}>'.format(self.id, self.team_name, self.time, self.country,
                                self.league, self.goals_scored, self.goals_conceded)