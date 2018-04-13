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
    def test_get_recent_for_no_args(self):
	"""should return if none of the args was given, they are optional and thus would not result in a error"""
	self.assertIsNone(get_team_recent_x())
	
    def test_get_recent_for_empty_args(self):
        """Such  cases should not happen; this is actually like useless repetitive testing"""
        self.assertIsInstance(get_team_recent_x('',''), dict)
        self.assertIn('home', get_team_recent_x('',''))
        self.assertIn('away', get_team_recent_x('',''))
        self.assertListEqual(get_team_recent_x('','')['home'], [])
        
    def test_get_recent_teams_for_invalid_args(self):
        """Raise errors in cases where the arguents are not as expected"""
        with self.assertRaises(ValueError):
            get_recent_team_x([], {})
            get_recent_team_x(-1, 2)
            
    def abstract_for_recent_function(alist, team_name):
        """
        :checks: the list len
        : the dates of the records
        : the order sequence
        """
        self.assertEqual(5, len(alist))
        for match in alist:
            self.assertGreater(match.date, datetime.date.today() - datetime.timedelta(days=(365 * 5)))
            self.assertIn(team_name, [match.team_one, match.team_two])
        # order_sequence
        date_golden_list = [match.date for match in alist].sort(reverse=True)
        self.assertListEqual([match.date for match in alist], date_golden_list)
        

    def test_get_recent_team_x_for_valid_query_with_one_team(self):
        """For a valid dataset i expect the right results given the home team"""
        result = get_recent_team_x() # remember to add the arg here
        self.assertIn('home', result.keys())
        self.assertIsInstance(result['home'], list)
        self.assertIsInstance(result['home'][0], Match)
        abstract_for_recent_function(result['home'], arg) # also feed in the arg from here
        for match in result['home']:
            self.assertEqual(arg, match.team_one)
        
    def test_get_recent_team_x_for_valid_query_with_away_team_arg(self):
        """for a valid arg qury: the away team"""
        result = get_recent_team_x() # remember to add the arg here also
        self.assertIn('away', result.keys())
        self.assertIsInstance(result['away'], list)
        self.assertIsInstance(result['away'][0], Match)
        abstract_for_recent_function(result['away'], arg) # remember to feed in the arg here to
        for match in result['away']:
            self.assertEqual(arg, match.team_two)
            
    def test_get_recent_team_x_for_valid_query_with_both_team_args_self(self):
        """just like in the above but with the added mile """
        result = get_recent_team_x(home_team=, away_team=)
        self.assertIn('away', result.keys())
        self.assertIsInstance(result['away'], list)
        self.assertIsInstance(result['away'][0], Match)
        abstract_for_recent_function(result['away'], arg)
        self.assertIn('home', result.keys())
        self.assertIsInstance(result['home'], list)
        self.assertIsInstance(result['home'][0], Match)
        abstract_for_recent_function(result['home'], arg)
        
    def test_get_recent_teams_for_the_x_factor(self):
        """the x factor provides a filter of how many records we wish to pull from the database"""
        home_result = get_recent_team_x(home_team=,x=3)
        self.assertEqual(3, len(home_result['home']))
        self.assertEqual(0, len(home_result['away']))
        away_result = get_recent_team_x(away_team=, x=3)
        self.assertEqual(3, len(home_result['away']))
        self.assertEqual(0, len(home_result['home']))
        result = get_recent_team_x(home_team=, away_team=,x=3)
        self.assertEqual(3, len(result['away']))
        self.assertEqual(3, len(result['home']))
        
    def test_get_recent_teams_for_absent_team(self):
        with self.raises(ValueError):
            get_recent_team_x(home_team="sasd")
            
    def test_get_recent_team_for_team_with_single_record(self):
        """need to make sure that the test data included only one match instance of this team"""
        result = get_recent_team_x(home_team=)
        self.assertEqual(1, len(result['home']))
        
        # what of overall specification
    def test_get_recent_team_with_overall_request(self):
        """should retrieve data in a manner such that for each match instance the given team plays either home or away"""
        result = get_recent_team_x(home_team=, x=5, overall=True)
        abstract_for_recent_function(result['home'], arg)
        
    def test_get_team_recent_for_date_filter(self):
        """Modify some diction values so that you have match instance that do not meet the date requirement threshhold and
        then wuery, pass determined if the number of recrds returned is corect"""