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

    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String())
    league_id = db.Column(db.Integer, db.ForeignKey('league.league_id'), nullable=False)
    logo = db.Column(db.String())
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
        return 'Team <{}{}{}{}{}{}{}>'.format(self.id, self.team_name, self.country, self.league_id)
    
    
class Country(db.Model):
    """
    One country holds or rather has several leagues
    a one to many relationship to that of the league models
    """
    country_id = db.Column(db.Integer, primary_key=True)
    country_name = db.column(db.String(), unique=True, nullable=False)
    flag_icon = db.Column(db.String, nullable=True)
    leagues = db.relationship('League', backref='country', lazy=True)
    
    def __repr__(self):
        """string serialisation"""
        return 'Country <{} {}>'.format(self.country_id, self.country_name)
    

class League(db.Model):
    """
    relation: one country holds several leagues
    one league holds several teams
    """
    league_id = db.Column(db.Integer, primary_key=True)
    league_name = db.Column(db.String())
    country_id = db.Column(db.Integer, db.ForeignKey('country.country_id'), nullable=False)
    teams = db.Relationship('Team', backref='league', lazy=True)
    
    def __repr__(self):
        """string serialisation"""
        return '<{} {}>'.format(self.league_id, self.league_name)
    
class Match(db.Model):
    """:realtion: one match will involves two teams"""
    match_id = db.Column(db.Integer, primary_key=True)
    team_one = db.column(db.integer, db.ForeignKey('team.team_id'), nullable=False)
    team_two = db.column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    time = db.Column(db.Time(), nullable=False)
    team_one_first_half_goals = db.Column(db.Integer, nullable=True)
    team_two_first_half_goals =db.Column(db.Integer, nullable=True)
    team_one_second_half_goals = db.Column(db.Integer, nullable=True)
    team_two_second_half_goals = db.Column(db.Integer, nullable=True)
    team_one_match_goals = db.Column(db.Integer, nullable=True)
    team_two_match_goals = db.Column(db.Integer, nullable=True)
    
    def __repr__(self):
        """This is pretty basic"""
        return '<{} {} {} {} {} {} {}>'.format(self.match_id, self.team_one, self.team_two, self.date, self.time, 
                                           self.team_one_match_goals, self.team_two_match_goals)
    
class Flagged(db.Model):
    """:relation just as that of a match, involves two matches"""
    flag_id = db.Column(db.Integer, primary_key=True)
    team_one = db.column(db.integer, db.ForeignKey('team.team_id'), nullable=False)
    team_two = db.column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
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
        return '<{} {} {} {} {}>'.format(self.flag_id, self.team_one, self.team_two, self.date, self.time)
    