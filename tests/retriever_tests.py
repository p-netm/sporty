import unittest, os
from app import create_app
from app.models import *
from app.gears.tango import get_teams_mutual, get_team_recent_x

# ah shit! we will have to have two test configurations which i find as very inconvient
# but for know thats the option i will implement due to time constraints

class RetrieverTests(unittest.TestCase):
    """we are testing two retrieve functions """
    def setUp(self):
        """set up the database as we create an application instance"""
        app = create_app('datatesting')
        app_context = app.app_context()
        app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        """we do not want to clear the database"""
        pass

    def test_retrieve_team_x_function_in_optimal_conditions(self):
        """as it was meant to be """
        # result len should be x
        # result time period

    def test_mutual_team_for_valid_data_set(self):
        """for a valid data set: no errors, runs as it is supposed to"""
        pass