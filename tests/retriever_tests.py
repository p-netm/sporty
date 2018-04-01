import unittest, os
from app import create_app
from app.models import *
from app.gears.tango import get_teams_mutual, get_team_recent_x
from app.gears.tango import saver_worker
from app.gears.scrapper import process_team_name
from .match import diction_list

class RetrieverTests(unittest.TestCase):
    """we are testing two retrieve functions """
    def setUp(self):
        """set up the database as we create an application instance"""
        app = create_app('testing')
        app_context = app.app_context()
        app_context.push()
        db.drop_all()
        db.create_all()
        for diction in diction_list:
            diction['home_team'] = process_team_name(diction['home_team'])
            diction['away_team'] = process_team_name(diction['away_team'])
            saver_worker(diction)

    def tearDown(self):
        """we do not want to clear the database"""
        # db.drop_all()

    def test_retrieve_team_x_function_in_optimal_conditions(self):
        """as it was meant to be """
        # result len should be x
        # result time period
        pass

    # def test_mutual_team_for_valid_data_set(self):
    #     """for a valid data set: no errors, runs as it is supposed to"""
    #     pass

    # what if there are no mutual matches that satisfy the time period
    # what if there are a few matches that satisfy the time period
    # MUTUAL: what if there are not enough  mutual matches
    # test where the home team is at away and viceversa
    # empty data