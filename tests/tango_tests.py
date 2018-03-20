import unittest
from app.gears import *


class TangoTests(unittest.TestCase):
    """refer: to app.gear.tango.py"""

    def setUp(self):
        """setup the test database"""
        db.create_all()
        

    def tearDown(self):
        """Teardown the test database"""
        db.drop_all()

    def test_saver_function_with_deformed_url(self):
        """if saver was offered a deformed url what does it do"""
        url = "asfbajsdb gaaf a daugf"
        with self.assertRaises(ValueError):
            saver(url)

    def test_saver_function_with_no_url(self):
        """what happens if tango.saver does not recieve this resource"""
        # it should run and requires a connection to the internet
        # 		self.assertTrue(saver())
        # 		self.assertTrue(Matches.query.all())
        pass

    def test_saver_worker_function(self):
        """see how well it responds to well formed data"""
        self.assertFalse(len(Match.query.all()))
        saver_worker(saverdata)
        self.assertTrue(len(Match.query.all()))
        self.assertEqual(6, len(Match.query.all()))

    def test_saver_worker_function_for_absent_data_mutual(self):
        """remove some expected fields and see how well it handles the deformation"""
        self.assertFalse(len(Match.query.all()))
        saver_worker(saverdatanomutual)
        self.assertEqual(1, len(Match.query.all()))
        
    def test_saver_worker_function_for_absent_data_(self):
        """deformed diction, occurence wil be rare"""
        self.assertFalse(len(Match.query.all()))
        saver_worker(saverdatadeformed) # say no date
        self.assertFalse(len(Match.query.all()))
        saver_worker(saverdatadeformed1) # say no country
        self.assertFalse(len(Match.query.all()))
        saver_worker(saverdatadeformed1) # say no league
        self.assertFalse(len(Match.query.all()))

    def test_worker_function_for_repeat_countries(self):
        """can this function detect that we have already added a certain country to our records"""
        self.assertFalse(len(Match.query.all()))
        saver_worker(saverdata)
        self.assertTrue(len(Match.query.all()))
        saver_worker(saverdatacountry)
        self.assertGreater(len(Match.query.all()), 12)
        self.assertEqual(1, len(Country.query.all()))
        

    def test_worker_function_for_repeat_league(self):
        """in the same spirit, does worker omit already present league names"""
        self.assertFalse(len(Match.query.all()))
        saver_worker(saverdata)
        self.assertTrue(len(Match.query.all()))
        saver_worker(saverdataleague)
        self.assertEqual(len(Match.query.all()), 12)
        self.assertEqual(1, len(League.query.all()))

    def test_worker_function_for_repeated_match(self):
        """what about the same match instances, as it will be so often for mutual matches"""
        self.assertFalse(len(Match.query.all()))
        saver_worker(saverdata)
        self.assertTrue(len(Match.query.all()))
        saver_worker(saverdata)
        self.assertEqual(6, len(Match.query.all()))

    def test_save_country(self):
        """check to see that the system does save country data as it is supposed to"""
        save_country(save['country'])
        self.assertEqual(len(Country.query.all()), 1)
        self.assertEqual(country.query.all()[0].country_name, save['country'])

    def test_save_country_duplicate_values(self):
        """save country: resave country"""
        save_country(save['country'])
        self.assertEqual(len(Country.query.all()), 1)
        assertFalse(save_country(save['country']))
        self.assertEqual(len(Country.query.all()), 1)

    def test_save_league_optimally(self):
        """does the system save league data the way that it is supposed to"""
        save_league(save['country'], save['league'])
        self.assertTrue(len(League.query.all()), 1)
        self.assertEqual(League.query.all()[0].league_name, save['league'])

        # now how about those leagues that belong to the same country
        save_league(save['country'], save1['league'])
        self.assertEqual(len(League.query.all()), 2)
        # load country and confirm that itholds backrefs to the two added leagues
        country = Country.query.filter_by(country_name=save['country']).first()
        self.assertEqual(len(country.leagues), 2)

    def test_save_duplicate_leagues(self):
        """how does the league saver deal with duplicate league entries"""
        save_league(save['country'], save['league'])
        self.assertTrue(len(League.query.all()), 1)
        self.assertFalse(save_league(save['country'], save['league']))
        self.assertTrue(len(League.query.all()), 1)
        country = Country.query.filter_by(country_name=save['country']).first()
        self.assertEqual(len(country.leagues), 1)

    def test_save_team_optimally(self):
        """test expectations"""
        self.assertTrue(len(Team.query.all()), 0)
        save_team(save['country'], save['league'], save['team'])
        self.assertTrue(len(Team.query.all()), 1)
        # add the same team to different leagues and see the response
        save_team(save['country'], save1['league'], save['team'])
        self.assertTrue(len(Team.query.all()), 2)
        league = League.query.filter_by(league_name=save1['league']).first()
        self.assertEqual(len(league.teams), 1)

    def test_save_team_with_duplicate_time(self):
        """teams is duplicate in the same league otherwise teams
        are not quaranteed to have unique names"""
        self.assertTrue(len(Team.query.all()), 0)
        save_team(save['country'], save['league'], save['team'])
        self.assertTrue(len(Team.query.all()), 1)
        self.assertFalse(save_team(save['country'], save['league'], save['team']))
        self.assertTrue(len(Team.query.all()), 1)

    def test_save_match_optimally(self):
        """under normal conditions does the save matches function perform as recomended"""
        self.assertFalse(len(Match.query.all()))
        save_match(save)
        self.assertTrue(len(Match.query.all()))

    def test_save_match_with_duplicate_values(self):
        """am getting tired of writing obvious statements such as this"""
        self.assertFalse(len(Match.query.all()))
        save_match(save)
        self.assertTrue(len(Match.query.all()))
        self.assertFalse(save_match(save))
        self.assertEqual(len(Match.query.all()), 1)

    def test_save_flagged_match_function_optimally(self):
        """And here i find myself again"""
        self.assertFalse(len(Flagged.query.all()))
        save_flagged(saveflagged, 'ov')
        self.assertTrue(len(Flagged.query.all()))
        save_flagged(saveflagged)
        self.assertEqual(len(Flagged.query.all()), 1)
        save_flagged(saveflagged, 'gg')
        self.assertEqual(len(Flagged.query.all()), 2)
        
    def test_save_flagged_match_with_conflicting_markets(self):
        """some markets are mutually exclusive and saving one should override the former"""
        self.assertFalse(len(Flagged.query.all()))
        save_flagged(saveflagged, '1')
        self.assertTrue(len(Flagged.query.all()))
        save_flagged(saveflagged, '2')
        self.assertEqual(len(Flagged.query.all()), 1)
        self.assertEqual(1, len(Flagged.query.filter(Flagged._2).all()))
        self.assertEqual(0, len(Flagged.query.filter(Flagged._1).all()))
          

    def test_save_flagged_match_function_for_duplicate_data(self):
        """and you know the drill right"""
        self.assertFalse(len(Flagged.query.all()))
        save_flagged(saveflagged, 'ng')
        self.assertTrue(len(Flagged.query.all()))
        save_flagged(saveflagged, 'ng')
        self.assertEqual(len(Flagged.query.all()), 1)
