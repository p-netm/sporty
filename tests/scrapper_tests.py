"""
		Solely test the scrapper functionality
"""
import unittest
from app.gears.scrapper import *
from validators import url


def create_file_path(filename):
    """abstract the path creation to the golden files"""
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'files', 'goldenfiles')
    if isinstance(filename, str):
        return os.path.join(base_dir, filename)
    else:
        raise TypeError("Filename is {}, expecting str".format(type(filename)))


def read_data(path):
    with open(path, 'r', encoding='utf-8') as handler:
        data = handler.read()
    return data


class Reckless(unittest.TestCase):
    def test_create_file_path(self):
        """check that any file path returned by the above function exists and that it is a html file"""
        path = create_file_path('nonesense')
        self.assertFalse(os.path.exists(path))
        path = create_file_path('awarded.html')
        self.assertTrue(os.path.exists(path))


class ScrapperTest(unittest.TestCase):
    """:Focus: the module app.gear.scrapper full functions"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_scrap_all_links(self):
        """See if the scrap dows return the expected number of links and also
        evaluate how well it handles errors.
        """
        # here i check only for  the expected number of tuples
        present_scrap = scrap_all_links(create_file_path('present_soccer_home.html'))
        self.assertIsInstance(present_scrap, list)
        # each instance is a tuples
        self.assertIsInstance(present_scrap[0], tuple)
        # each scrapped element is a full blown valid url without the #odds
        self.assertTrue(url(present_scrap[0][2]))
        self.assertTrue(url(present_scrap[2][2]))
        # should not have the fragment #odds at the end of the url
        # we also do not create a beatiful soup object here as we do in the other test fixtures
        # because the scrap_all_links function does that by itself.
        sample_url = present_scrap[0][0]
        self.assertEqual(sample_url.find('#odds'), -1)
        self.assertEqual(len(present_scrap), 200)
        self.assertEqual(len(scrap_all_links(create_file_path('past_soccer_home.html'))), 187)
        self.assertEqual(len(scrap_all_links(create_file_path('future_soccer_home.html'))), 835)

    def test_date_from_string(self):
        """refer to method declaration"""
        sample_string = 'Today, 26 Jun 2017, 00:00++++'
        deformed_string = 'Today, 26 Jun 207, 00:00++++'
        time_deformed_string = 'Today, 26 Jun 2017, 0:00++++'
        no_effect = ' 26 Jun 2017, 00:00++++'
        date = datetime.date(2018, 6, 26)
        time = datetime.time()
        self.assertIsInstance(date_from_string(sample_string), tuple)
        self.assertIsInstance(date_from_string(no_effect), tuple)
        with self.assertRaises(PatternMatchError):
            date_from_string(deformed_string)
            date_from_string(time_deformed_string)
        self.assertIsInstance(date_from_string(sample_string)[0], datetime.date)
        self.assertIsInstance(date_from_string(sample_string)[1], datetime.time)

    def assert_things(self, diction):
        """am not even sure that this works or even if this is legal"""
        self.assertIn('league', diction.keys())
        self.assertIn('country', diction.keys())
        self.assertIn('home_team', diction.keys())
        self.assertIn('away_team', diction.keys())
        self.assertIn('date', diction.keys())
        self.assertIn('time', diction.keys())
        self.assertIn('home_first_half_goals', diction.keys())
        self.assertIn('away_first_half_goals', diction.keys())
        self.assertIn('home_second_half_goals', diction.keys())
        self.assertIn('away_second_half_goals', diction.keys())
        self.assertIn('home_match_goals', diction.keys())
        self.assertIn('away_match_goals', diction.keys())

    def test_get_specific_match_details_for_played_match(self):
        """This is more than a unit test"""
        played_soup = BeautifulSoup(read_data(create_file_path('played.html')), 'html.parser')
        result = get_specific_match_details(played_soup)
        self.assert_things(result)
        # type and value checks
        self.assertEqual(result['league'], 'First Division')
        self.assertEqual(result['country'], 'Cyprus')
        self.assertEqual(result['home_team'], 'APOEL')
        self.assertEqual(result['away_team'], 'AEK Larnaca')
        self.assertEqual(result['date'], datetime.date(2018, 3, 11))
        self.assertEqual(result['time'], datetime.time(14, 0))
        self.assertEqual(result['home_first_half_goals'], 0)
        self.assertEqual(result['home_second_half_goals'], 0)
        self.assertEqual(result['away_first_half_goals'], 0)
        self.assertEqual(result['away_second_half_goals'], 0)
        self.assertEqual(result['home_match_goals'], 0)
        self.assertEqual(result['away_match_goals'], 0)

    def test_get_specific_match_details_for_abandoned_match(self):
        """do abandoned matches html files abide by the same formats as the rest of them"""
        abandoned_soup = BeautifulSoup(read_data(create_file_path('abandoned.html')), 'html.parser')
        result = get_specific_match_details(abandoned_soup)
        self.assert_things(result)
        # a brief check of value and types -> some attributes i wil not check since i do not expect them to have changed
        self.assertEqual(result['date'], datetime.date(2018, 3, 11))
        self.assertEqual(result['time'], datetime.time(17, 30))
        self.assertEqual(result['home_first_half_goals'], 0)
        self.assertEqual(result['home_second_half_goals'], 0)
        self.assertEqual(result['away_first_half_goals'], 0)
        self.assertEqual(result['away_second_half_goals'], 0)

    def test_get_specific_match_details_for_penalties_match(self):
        """test fixture for future matches html files"""
        penalty_soup = BeautifulSoup(read_data(create_file_path('penalties.html')), 'html.parser')
        result = get_specific_match_details(penalty_soup)
        self.assert_things(result)
        # remember the system only recognizes result up until end of regulation time
        # where the full scores defer from the adition of the respective half scores, then that means  that the
        # respective ficture was played into extra time.
        self.assertEqual(result['league'], 'Czech Cup Women')
        self.assertEqual(result['home_first_half_goals'], 2)
        self.assertEqual(result['home_second_half_goals'], 0)
        self.assertEqual(result['away_first_half_goals'], 0)
        self.assertEqual(result['away_second_half_goals'], 2)

    def test_get_specific_match_details_for_postponed_match(self):
        """what about when we have a html file for a fixture that was postpponed"""
        post_soup = BeautifulSoup(read_data(create_file_path('postponed.html')), 'html.parser')
        result = get_specific_match_details(post_soup)
        self.assert_things(result)
        self.assertEqual(result['home_first_half_goals'], None)
        self.assertEqual(result['home_second_half_goals'], None)
        self.assertEqual(result['away_first_half_goals'], None)
        self.assertEqual(result['away_second_half_goals'], None)
        self.assertEqual(result['home_match_goals'], None)
        self.assertEqual(result['away_match_goals'], None)

    # the test below requires a live connection to the internet to run.

    # 	def test_retrieve_mutual_matches_data_for_played_match(self):
    # 		"""we just check that the mutual key has a value of the required format"""
    # 		played_soup = BeautifulSoup(read_data(create_file_path('played.html')), 'html.parser')
    # 		result = retrieve_mutual_matches_data(played_soup)
    # 		self.assertEqual(type(result), dict)
    # 		self.assertIn('mutual', result.keys())
    # 		self.assertIsInstance(result['mutual'], list)
    # 		self.assertIsInstance(result['mutual'][0], dict)
    # 		match_instance = result['mutual'][0]
    # 		self.assert_things(match_instance)

    def test_no_data_mutual_matches_data(self):
        """what if the fed in html file does not have the data required"""
        gold_soup = BeautifulSoup(read_data(create_file_path('gold.html')), 'html.parser')
        with self.assertRaises(TagError):
            result = retrieve_mutual_matches_data(gold_soup)

    def test_no_data_soccer_home_page(self):
        """lets see what is the responde of the scrap all links function when it has
        nothing to scrap"""
        gold_path = create_file_path('gold.html')
        with self.assertRaises(TagError):
            scrap_all_links(gold_path)

    def test_scrap_past_matches_data_with_full_score_only(self):
        """Past data might occur in a unexpected format where the full score is present but the
        half scores are absent"""
        # the system should work normally for such scenarios: ignoring the absent data and saving what it has
        played_soup = BeautifulSoup(read_data(create_file_path('fullscoreonly.html')), 'html.parser')
        result = get_specific_match_details(played_soup)
        self.assert_things(result)
        self.assertEqual(result['league'], 'OFB Cup')
        self.assertEqual(result['country'], 'Austria')
        self.assertEqual(result['home_team'], 'FAC Wien')
        self.assertEqual(result['away_team'], 'Kapfenberg')
        self.assertEqual(result['date'], datetime.date(2010, 8, 13))
        self.assertEqual(result['time'], datetime.time(20, 0))
        self.assertEqual(result['home_first_half_goals'], None)
        self.assertEqual(result['home_second_half_goals'], None)
        self.assertEqual(result['away_first_half_goals'], None)
        self.assertEqual(result['away_second_half_goals'], None)
        self.assertEqual(result['home_match_goals'], 1)
        self.assertEqual(result['away_match_goals'], 2)

    def test_process_league(self):
        """Maybe we shooul have some sort of standard when cleaning up the url so as to make
        sure trivial hings such as seasons do not confuse our scrapper"""
        self.assertEqual(process_league('OFB Cup 2010/2011'),'OFB Cup')
        self.assertEqual('Erste Liga', process_league('Erste Liga 2016/2017'))

    def test_process_team_name(self):
        """Some team names are saved as variations of themselves due  to having unnecessary semantic suffixes
        added to them. We might be dealing with only onse simple case here the team_name has a suffix of its country"""
        self.assertEqual('FAC Wien', process_team_name('FAC Wien (Aut)'))
        self.assertEqual('Austria Vienna', process_team_name('Austria Vienna (Aut)'))
