import unittest

from sportstats.app.gears.scrapper import date_from_string, datetime, splitter, one_x_2, start_conveyer


class BeatifulSoupTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_date_from_string_function(self):
        self.assertTrue(date_from_string('Today, 26 Jun 2017, 00:00++++'))
        # check what happens should the format change
        with self.assertRaises(Exception) as context:
            date_from_string('Today, Jun 2017, 00:00++++')
            self.assertTrue(context)
        self.assertTrue(type(date_from_string('Today, 26 Jun 2017, 00:00++++')) is datetime)
        _date = date_from_string('Today, 26 Jun 2017, 00:00++++')
        self.assertEqual(_date.hour, 0)
        self.assertEqual(_date.minute, 0)
        self.assertEqual(_date.year, 2017)
        self.assertEqual(_date.month, 6)
        self.assertEqual(_date.day, 26)

class ScoreFunctions(unittest.TestCase):
    def setUp(self):
        score = "2-3"
        self.score = splitter(score)
        self.draw = splitter("1-1")
        self.home = splitter("1-0")
        self.diction = {'mutual': [{'home_team': 'Arsenal', 'away_team': 'Manchester United', 'full_time_score': '2-3'},
                              {'home_team': 'Arsenal', 'away_team': 'Manchester United', 'full_time_score': '2-3'},
                              {'home_team': 'Arsenal', 'away_team': 'Manchester United', 'full_time_score': '2-3'},
                              {'home_team': 'Arsenal', 'away_team': 'Manchester United', 'full_time_score': '2-3'}],
                   'time': 21582346, 'home_team': 'Arsenal', 'away_team': 'Manchester United', 'full_time_score': '2-3'}


    def tearDown(self):
        pass

    def test_splitter_method(self):
        score = "2-3"
        new_score = splitter(score)
        self.assertTrue(type(new_score), dict)
        self.assertTrue(len(new_score) == 2)

    def test_one_x_2_function(self):
        self.assertEqual(one_x_2(self.score), 0)
        self.assertEqual(one_x_2(self.draw), 'x')
        self.assertEqual(one_x_2(self.home), 1)

    def test_relative_win(self):
        pass

    def test_conveyer_method(self):
        result = (start_conveyer(self.diction))
        self.assertTrue(start_conveyer(self.diction) is not None)
        for string in result:
            self.assertTrue(string)