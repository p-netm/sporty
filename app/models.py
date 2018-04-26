"""Definition of all the class models that wil be mapped onto a daabase
unlike for the eanmble ts, te eanmble sp will be a bit different due the increased level of operations and 
data manipulations involved in getting to a reasonable fixture prediction analysis
"""
from . import db
from marshmallow import Schema, fields


class Team(db.Model):
    """Represents the data that will be saved about a specific team

    a representation of the aspects that are most important in this preliminary
    survey, this aspects will be added to the data csv file
    """
    team_name = db.Column(db.String(), unique=True, primary_key=True)
    logo = db.Column(db.String(), nullable=True)  # can set unique to true
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
    
class TeamSchema(Schema):
    team_name = fields.Str()
    logo = fields.Str()
    
    
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
    """:realation: one match will involves two teams"""
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
        return '<{} {} {} {} {} 1.{} x.{} 2.{}>'.format(self.flag_id, self.team_one, self.team_two, self.date, self.time,
                                                        self._1, self._x, self._2)

class FlaggedSchema(Schema):
    team_one = fields.Str()
    team_two = fields.Str()
    date = fields.Date()
    time = fields.Time()
    
class SubscribedEmail(db.Model):
    email = db.Column(db.String(), primary_key=True)
    
    def __repr__(self):
        return '<email {}>'.format(self.email)
    