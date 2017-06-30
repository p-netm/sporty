import unittest
from sportstats.app.scrapper import date_from_string, re, datetime


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